#import OpenGL.GL as gl
import OpenGL.GL.shaders
from OpenGL.GL import *

#import glfw
import ctypes
#from pyopengltk import OpenGLFrame
import numpy as np
import glm
import random
from PIL import Image,ImageDraw
from math import sin,cos,sqrt,pi
import time
from mychem_functions import make_sphere_vert,make_cube2,print_bytes_with_highlights
from mychem_data import cube_vertices
from mychem_atom import Node,AtomC,NodeC
from array import array
from mesh import Mesh
import threading
import json
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer
#from PyQt5.QtGui import QOpenGLWindow,
#from OpenGL.GL import *
from shader import Shader,ComputeShader

class GLWidget(QOpenGLWidget):
    def __init__(self,space):
        super().__init__()
        self.space = space
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def initializeGL(self):
        """Initalize gl states when the frame is created"""
        print("init gl")
        #self.w
        #self.setMinimumSize(self.width, self.height)
        
        glViewport(0, 0, self.width(), self.height())
        glClearColor(0.3, 0.3, 0.3, 0.0)
        glEnable(GL_DEPTH_TEST)
        glBlendEquation(GL_FUNC_ADD)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE,GL_ZERO)
        #glEnable(GL_CULL_FACE);
        #glCullFace(GL_FRONT); 
        #glFrontFace(GL_CW) 
        #glEnable(GL_DEBUG_OUTPUT)
        #glEnable(GL_CULL_FACE); 
        #glEnable(GL_FRAMEBUFFER_SRGB);
        #glEnable(GL_DEPTH_TEST)
        #glEnable (GL_LINE_SMOOTH);    
        #glfwWindowHint(GLFW_SAMPLES, 4);
        #glEnable(GL_MULTISAMPLE); 
        self.iconic = False
        self.nearatomsmax = 5000
        self.LOCALSIZEX = 64
        self.nearflag = False
        self.drawnodes =  True
        self.update_uniforms = True
        self.CUBESIZE = 1280

        self.shader =  Shader("atom_vertex1.glsl", "atom_frag1.glsl")
        
        params = {"NEARATOMSMAX":str(self.nearatomsmax) ,
                  "LOCALSIZEX":str(self.LOCALSIZEX),
                  "MAXVEL":str(self.space.MAXVELOCITY)
                  }
        self.compute_shader = ComputeShader("compute.glsl", params)

        params = {"LOCALSIZEX":str(self.LOCALSIZEX)}
        self.select_shader = ComputeShader("select.glsl", params)
        
        self.init_loc()

        self.cameraUp = glm.vec3(0,1,0)
        self.cameraFront = glm.vec3(0.5,0.5,-1)
        self.cameraPos = glm.vec3(0.5,0.5,2)
        self.cubemap_cameraPos = glm.vec3(1.0,0.5,1.0)        
        self.cameraTarget = glm.vec3(0.5,0.5,0.5)
        self.lightPos = glm.vec3(1.0,0.5,1.0)

        #self.cameraDirection = glm.normalize(self.cameraPos - self.cameraTarget)
        self.keypressed = []
        self.lastframe_time= time.time()
        self.lastX = 500
        self.lastY = 300
        self.yaw = -90
        self.pitch = 0 
        self.fov = 45
        self.factor = 0.001
        self.curpos = glm.vec3(0.,0.,0.)
        self.sphere_vertices = np.array(make_sphere_vert(1,20), dtype=np.float32)
        self.sphere_vertices2 = np.array(make_sphere_vert(1,5), dtype=np.float32)
        self.cube_vertices = np.array(make_cube2(), dtype=np.float32)
        #np.array(make_cube2(), dtype=np.float32)
        #cameraRight = glm.normalize(glm.cross(up, cameraDirection))
        #cameraUp = glm.cross(cameraDirection, cameraRight)
        self.create_objects()
        self.setup_framebuffer()
        self.space.atoms2compute()
        self.start = time.time()
        self.nframes = 0          
        self.rframes = 0
        self.initok = True

        
    def setup_framebuffer(self):
        print("setup additional framebuffer")
        # Создаем framebuffer
        self.framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        # Создаем renderbuffer для цвета
        color_buffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, color_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGB, self.CUBESIZE, self.CUBESIZE)

        # Прикрепляем renderbuffer к framebuffer
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color_buffer)

        # Создаем renderbuffer для глубины
        depth_buffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.CUBESIZE, self.CUBESIZE)

        # Прикрепляем renderbuffer глубины к framebuffer
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buffer)

        # Проверяем, что framebuffer готов
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer is not complete!")


    def atoms2ssbo(self):
        self.makeCurrent()
        self.N = len(self.space.atoms)
        print(f"  Atoms2ssbo N={self.N}")
        ac = AtomC()
        nc = NodeC()
        if self.N>0:
            a_data = bytearray()
            for a in self.space.atoms:
                ac.to_ctypes(a)
                abytearray =  bytearray(ac)               
                a_data += abytearray
                for n in a.nodes:
                    nc.to_ctypes(n, self.space)
                    nbytearray = bytearray(nc)
                    a_data += nbytearray
                for i in range(0,5-len(a.nodes)):
                    nbytearray = bytearray(ctypes.sizeof(NodeC))
                    a_data += nbytearray
        else:
            a_data = bytearray(1)
        datasize = len(a_data)
        a_data = np.array(a_data,dtype=np.byte)
#        print_bytes_with_highlights(a_data,[(ctypes.sizeof(AtomC)+9*4,4)])
        print(f"  buffer size={datasize}")
        self.atoms_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.atoms_buffer)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer);
       
        glBufferData(GL_SHADER_STORAGE_BUFFER, datasize, a_data , GL_DYNAMIC_DRAW);
        self.atoms_buffer2 = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.atoms_buffer2)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.atoms_buffer2);
        glBufferData(GL_SHADER_STORAGE_BUFFER, datasize, None , GL_DYNAMIC_DRAW);
    
        #nearbuffer
        self.near_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.near_buffer)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.near_buffer);
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.N*4*(self.nearatomsmax+1), None , GL_DYNAMIC_DRAW);
        self.nearflag = True    

        #far field buffer
        self.far_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.far_buffer)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.far_buffer);
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.N*4, None , GL_DYNAMIC_DRAW);

        # real pos buffer
        self.rpos_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.rpos_buffer)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.rpos_buffer);
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.N*4*4*6, None , GL_DYNAMIC_DRAW);


        self.qshift_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.qshift_buffer)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 6, self.qshift_buffer);
        zero = np.zeros(self.N*4*6,dtype=np.byte)
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.N*4*6, zero , GL_DYNAMIC_DRAW); 
        



        #spin set
        self.compute_shader.use()
        self.compute_shader.setInt("stage",1) # rpos of nodes and atom q
        self.compute_shader.run(int(len(self.space.atoms)/self.LOCALSIZEX)+1,1,1)        
        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
        self.compute_shader.setInt("stage",3) #autospinset
        self.compute_shader.run(int(len(self.space.atoms)/self.LOCALSIZEX)+1,1,1)        
        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)

        self.compute_shader.setFloat("NEARDIST",self.space.NEARDIST)
        self.compute_shader.setInt("stage",2) #nearatoms
        self.compute_shader.run(int(len(self.space.atoms)/self.LOCALSIZEX)+1,1,1)        
        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)

        self.compute_shader.setInt("stage",4)   # bonded state
        self.compute_shader.run(int(len(self.space.atoms)/self.LOCALSIZEX)+1,1,1)        
        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)


        self.set_compute_uniforms()
        #self.doneCurrent()


    def ssbo2atoms(self):
        self.makeCurrent()
        self.N = len(self.space.atoms)
        print(f"  ssbo2atoms N={self.N}")
        asize = ctypes.sizeof(AtomC)+ctypes.sizeof(NodeC)*5
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.atoms_buffer)
        a_data8 = glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self.N*asize)
        #print_bytes_with_highlights(a_data8,[(ctypes.sizeof(AtomC)+9*4,4)])
        print("  getbuffersubdata size=", self.N*asize)
        #print("sizeof AtomC", ctypes.sizeof(AtomC))
        #print("sizeof NodeC", ctypes.sizeof(NodeC))
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
        self.doneCurrent()
        offset = 0
        self.space.Ek = 0
        for i in range(0,self.N):
            a = self.space.atoms[i]
            abytearray = a_data8[offset:offset+ctypes.sizeof(AtomC)]
            ac = AtomC.from_buffer(abytearray)
            ac.from_ctypes(a)
            self.space.Ek += a.m*glm.dot(a.v,a.v)/2.0
            offset+= ctypes.sizeof(AtomC)
            for n in a.nodes:
                nbytearray = a_data8[offset:offset+ctypes.sizeof(NodeC)]
                nc = NodeC.from_buffer(nbytearray)
                nc.from_ctypes(n,self.space)
                offset+= ctypes.sizeof(NodeC)
            for i in range(0,5-len(a.nodes)):
                offset+= ctypes.sizeof(NodeC)




    def init_loc(self):
            self.compute_shader.init_uniforms(["stage", "box", "iTime",
                                                "bondlock", "gravity", "redox",
                                                "shake", "TDELTA", "BOND_KOEFF",
                                                "INTERACT_KOEFF", "REPULSION_KOEFF1", "REPULSION_KOEFF2",
                                                "ATTRACTION_KOEFF",  "ROTA_KOEFF", "MASS_KOEFF",
                                                "FIELD_KOEFF",  "NEARDIST", "NODEDIST", "HEAT",
                                                "highlight_unbond",  "sideheat", "efield", "test"
                                               ]
                                              )
            self.shader.init_uniforms([ "model", "objectColor", "view", "projection", "mode", "nodeindex",
                                         "lightPos", "transparency" 
                                      ])

    def create_objects(self):
        print("create objects")
        self.atomMesh = Mesh(self.sphere_vertices)
        self.atomMesh.setShader(self.shader)
        self.atomMesh.setup()
        self.nodeMesh = Mesh(self.sphere_vertices2)
        self.nodeMesh.setShader(self.shader)
        self.nodeMesh.setup()
        self.containerMesh = Mesh(self.cube_vertices)
        self.containerMesh.setShader(self.shader)
        self.containerMesh.setup()
        model =  glm.mat4()
        model =  glm.scale(model,self.space.box/glm.vec3(1/self.factor))
        model =  glm.scale(model, glm.vec3(0.5,0.5,0.5))
        model =  glm.translate(model, glm.vec3(1, 1, 1))
        self.containerMatrix = model
        

    def updateContainerSize(self):
        if not self.containerMesh: return
        model =  glm.mat4()
        model =  glm.scale(model,self.space.box/glm.vec3(1/self.factor))
        model =  glm.scale(model, glm.vec3(0.5,0.5,0.5))
        model =  glm.translate(model, glm.vec3(1, 1, 1))
        self.containerMatrix = model

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        self.shader.use()
        self.shader.setMatrix4("view", self.view)
        self.shader.setMatrix4("projection", self.projection)
        self.shader.set3f("lightPos", self.lightPos.x, self.lightPos.y, self.lightPos.z)

        # draw container            
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE )
        self.shader.setMatrix4("model",self.containerMatrix)
        self.shader.set4f("objectColor",1,1,1,1)
        self.containerMesh.drawQuads()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL )

        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)

        #render merge_atom
        #if len(self.space.merge_atoms)>0:
        if self.main.merge_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            for a in self.space.merge_atoms:
                pos = glm.vec3(a.pos)
                pos *= self.factor
                model =  glm.translate(pos)
                model =  glm.scale(model,glm.vec3(1)*self.factor*a.r)
                self.shader.setMatrix4("model", model)
                self.shader.set4f("objectColor",a.color[0],a.color[1],a.color[2],a.color[3])
                self.atomMesh.draw()
                #render merge atoms nodes
                for n in a.nodes:
                    #pos = a.rot * n.pos
                    pos = a.pos + a.rot * n.pos
                    #pos -= self.space.merge_center
                    #pos = self.space.merge_rot * pos
                    #pos += self.space.merge_pos
                    pos *= self.factor
                    model =  glm.translate(pos)
                    model =  glm.scale(model,glm.vec3(1)*self.factor*0.1*a.r)
                    if n.type==2:
                        color = glm.vec4(30/256.0,144/255.0,1.0,1.0)
                    else:
                        if n.bonded:
                            color = (0.0,1.0,0.0,1.0) 
                        else:
                            color = (1.0,1.0,1.0,1.0) 
                    self.shader.setMatrix4("model", model)
                    self.shader.set4f("objectColor",color[0],color[1],color[2],color[3])
                    self.nodeMesh.draw()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # render computed atoms
        if self.N>0:
            self.atomMesh.bind()
            if self.space.tranparentmode:
                self.shader.setInt("transparency",1)
            self.shader.setInt("mode",1)
            glDrawArraysInstanced(GL_TRIANGLES, 0, int(self.sphere_vertices.size/6), len(self.space.atoms))
            if self.drawnodes:
                self.shader.setInt("mode",2)
                self.nodeMesh.bind()
                for i in range(0,5):
                        self.shader.setInt("nodeindex",i)
                        glDrawArraysInstanced(GL_TRIANGLES, 0, int(self.sphere_vertices2.size/6), len(self.space.atoms))

            #draw transparent atoms after opaque
            if self.space.tranparentmode:
                glEnable(GL_BLEND)
                glDepthMask(GL_FALSE)
                self.atomMesh.bind()
                self.shader.setInt("transparency",2)
                self.shader.setInt("mode",1)
                glDrawArraysInstanced(GL_TRIANGLES, 0, int(self.sphere_vertices.size/6), len(self.space.atoms))
                self.shader.setInt("transparency",0)
                glDisable(GL_BLEND)
                glDepthMask(GL_TRUE)
        
        self.shader.setInt("mode",0)
        glBindVertexArray( 0 )



        #render selection
        if self.space.select_mode==1:
            for i in self.space.selected_atoms:
                a = self.space.atoms[i]
                model =  glm.mat4()
                model =  glm.translate(model, a.pos * self.factor  )
                model =  glm.scale(model, glm.vec3(a.r * self.factor*1.1))
                color = (0,1.0,0,1.0)
                self.shader.setMatrix4("model", model)
                self.shader.set4f("objectColor",color[0],color[1],color[2],color[3])

                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE );
                self.atomMesh.draw()
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL );
                if len(self.space.selected_atoms)<=2 and a.nodeselect!=-1:
                    n = a.nodes[a.nodeselect]
                    pos = a.rot * n.pos *1.1
                    pos += a.pos
                    model =  glm.mat4()
                    model =  glm.translate(model, pos * self.factor  )
                    model =  glm.scale(model,glm.vec3(self.factor*0.2*a.r))
                    color = (1.0,0.0,1.0,1.0) 
                    self.shader.setMatrix4("model", model)
                    self.shader.set4f("objectColor",color[0],color[1],color[2],color[3])
                    self.nodeMesh.draw()                
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL );


        glDisable(GL_CULL_FACE);
        glUseProgram(0)


    def set_compute_uniforms(self):
            s = self.compute_shader
            s.use()
            s.setInt("bondlock", self.space.bondlock )
            glUniform3fv(s.loc["box"], 1, glm.value_ptr(self.space.box))
            s.setInt("iTime", self.space.t )
            s.setFloat("TDELTA", self.space.TDELTA )
            s.setInt("gravity",self.space.gravity)
            s.setInt("redox",self.space.redox)
            s.setInt("shake",self.space.shake)
            s.setFloat("BOND_KOEFF",self.space.BOND_KOEFF)
            s.setFloat("INTERACT_KOEFF",self.space.INTERACT_KOEFF)
            s.setFloat("REPULSION_KOEFF1",self.space.REPULSION_KOEFF1)
            s.setFloat("REPULSION_KOEFF2",self.space.REPULSION_KOEFF2)
            s.setFloat("ATTRACTION_KOEFF",self.space.ATTRACTION_KOEFF)
            s.setFloat("ROTA_KOEFF",self.space.ROTA_KOEFF)
            s.setFloat("MASS_KOEFF",self.space.MASS_KOEFF)
            s.setFloat("FIELD_KOEFF",self.space.FIELD_KOEFF)
            s.setFloat("NEARDIST",self.space.NEARDIST)
            s.setFloat("NODEDIST",self.space.NODEDIST)
            s.setFloat("HEAT",float(self.space.heat))
            s.setInt("sideheat",self.space.sideheat)
            s.setInt("efield",self.space.efield)
            s.setInt("test",self.space.test)
            s.setInt("highlight_unbond",self.space.highlight_unbond)
            print("set compute vars")

    def compute(self):
        # gpu compute atoms
        self.atomMesh.bind()

        if self.update_uniforms:
            self.set_compute_uniforms()
            self.update_uniforms=False
        if not self.space.pause:
            self.compute_shader.use()

            for i in range(0,self.space.update_delta):
                    self.space.t+=1
                    self.compute_shader.setInt("stage",1) #calc q and rpos of nodes
                    self.compute_shader.run(int(self.N/self.LOCALSIZEX)+1,1,1)        
                    glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
                    if self.space.t%(int(self.space.NEARDIST/2.0))==0 or self.nearflag==True:  #near field calc
                        self.nearflag = False
                        self.compute_shader.setInt("stage",2)   #calc near atoms  and far field
                        self.compute_shader.run(int(self.N/self.LOCALSIZEX)+1,1,1)        
                        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
                        #self.compute_shader.setInt("stage",4)   # bonded state
                        #self.compute_shader.run(int(len(self.space.atoms)/self.LOCALSIZEX)+1,1,1)        
                        #glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)

                    #self.compute_shader.setInt("stage",4) #bond state
                    #self.compute_shader.run(int(len(self.space.atoms)/self.LOCALSIZEX)+1,1,1)        
                    #glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)

                    self.compute_shader.setInt("stage",5)  #main
                    self.compute_shader.run(int(self.N/self.LOCALSIZEX)+1,1,1)        
                    glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
                    self.atoms_buffer,self.atoms_buffer2 = self.atoms_buffer2,self.atoms_buffer
                    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer)
                    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.atoms_buffer2)
                    if self.space.action:
                        self.space.action(self.space)   
            glUseProgram(0)


    def recordframe(self,pix,rframes):
        img = Image.frombytes("RGB", (self.width(),self.height()), pix)
        img2 = img.transpose(method=Image.FLIP_TOP_BOTTOM)
        img3 = ImageDraw.Draw(img2)
        img3.text((10,10),str(rframes))
        img2.save("output/frame"+str(rframes)+".png")

    def recordframe3d(self,pix,rframes):
        cubemap_image = Image.new("RGB", (self.CUBESIZE * 3, self.CUBESIZE * 2))
        for i in range(6):
            img = Image.frombytes("RGB", (self.CUBESIZE,self.CUBESIZE), pix[i])
            img2 = img.transpose(method=Image.FLIP_TOP_BOTTOM)
            x = (i % 3) * self.CUBESIZE  # Столбец (0, 1, 2)
            y = (i // 3) * self.CUBESIZE  # Строка (0 или 1)
            cubemap_image.paste(img2, (x,y))
        cubemap_image.save("output/frame"+str(rframes)+".png")              


    def recorddata(self,rframes):
        data = self.space.make_export()
        f = open("output/data/frame"+str(rframes)+".json","w")
        f.write(json.dumps(data))
        f.close()



    def paintGL(self):
        """Render a single frame"""
        #glClear(GL_COLOR_BUFFER_BIT)
        self.N = len(self.space.atoms)
        front = ( cos(glm.radians(self.pitch))*cos(glm.radians(self.yaw)),
                 sin(glm.radians(self.pitch)),
                 cos(glm.radians(self.pitch))*sin(glm.radians(self.yaw)),
                )
        self.cameraFront = glm.normalize(front)
        self.view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        self.lightPos = glm.vec3(self.cameraPos.x+self.view[0,0]+self.view[0,1],
                                            self.cameraPos.y+self.view[1,0]+self.view[1,1],
                                            self.cameraPos.z+self.view[2,0]+self.view[2,1])
        a = self.width()
        b=  self.height()
        self.projection = glm.perspective(glm.radians(self.fov), a/b, 0.01,20.0)

        #glBindFramebuffer(GL_FRAMEBUFFER, None)
        glViewport(0, 0, self.width(), self.height())
        self.render()
        self.compute()

        if (self.space.recording or self.space.record_data) and not self.space.pause:
            if self.space.recording:
                pix = glReadPixels(0,0,self.width(), self.height(),GL_RGB,GL_UNSIGNED_BYTE)
                thread = threading.Thread(target=self.recordframe,args=(pix,self.rframes))
                thread.daemon = True
                thread.start()
            if self.space.record_data:
                self.space.compute2atoms()
                thread = threading.Thread(target=self.recorddata,args=(self.rframes,))
                thread.daemon = True
                thread.start()
            self.rframes+=1

        if self.space.recording3D and not self.space.pause:
                pix = [None] *6
                directions = [
                    (glm.vec3(1, 0, 0), glm.vec3(0, -1, 0)),  # Право
                    (glm.vec3(-1, 0, 0), glm.vec3(0, -1, 0)), # Лево
                    (glm.vec3(0, -1, 0), glm.vec3(0, 0, -1)), # Вниз
                    (glm.vec3(0, 1, 0), glm.vec3(0, 0, 1)),   # Вверх
                    (glm.vec3(0, 0, 1), glm.vec3(0, -1, 0)),  # Вперед
                    (glm.vec3(0, 0, -1), glm.vec3(0, -1, 0)), # Назад
                ]                
                glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
                glViewport(0, 0, self.CUBESIZE, self.CUBESIZE)
                self.projection = glm.perspective(glm.radians(90.0), 1.0, 0.001, 100.0)
                self.lightPos = glm.vec3(self.cubemap_cameraPos.x, self.cubemap_cameraPos.y, self.cubemap_cameraPos.z)
                self.lightPos.y -=0.5
                self.lightPos.x -=0.2
                for i, (direction, up) in enumerate(directions):
                    self.view = glm.lookAt(self.cubemap_cameraPos, self.cubemap_cameraPos + direction, up)
                    self.render()
                    pix[i] = glReadPixels(0,0,self.CUBESIZE, self.CUBESIZE,GL_RGB,GL_UNSIGNED_BYTE)
                #dirs = ['right', 'left', 'bottom', 'top', 'front', 'back']
                #img2.save("output/frame"+str(self.rframes)+"_"+dirs[i]+".png")

                thread = threading.Thread(target=self.recordframe3d,args=(pix,self.rframes))
                thread.daemon = True
                thread.start() 
                glBindFramebuffer(GL_FRAMEBUFFER, 0)   
                self.rframes+=1

        self.curframe_time = time.time()
        self.framedelta = self.curframe_time - self.lastframe_time 
        self.lastframe_time = self.curframe_time
        throttle = 1/40 - self.framedelta
        if throttle>0:
            time.sleep(throttle)
        self.nframes += 1
#        print("fps",self.nframes / tm, end="\r" )
        if self.nframes%50 == 0:
            if self.framedelta!=0:
                tm = time.time() - self.start
                self.status_bar.setFPS(self.nframes/tm)

    def expand_selection(self, selected_atoms):
        sel_time_begin = time.time()
        self.makeCurrent()
        self.select_shader.use()
        #print("atoms N=", self.N)
        int_array = np.array(selected_atoms, dtype=np.int32)
        int_array = int_array.tobytes()
        sel_buffer = glGenBuffers(1)
        sel_buffer2 = glGenBuffers(1)
        counter_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, sel_buffer)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 7, sel_buffer)
        glBufferData(GL_SHADER_STORAGE_BUFFER, len(int_array), int_array , GL_DYNAMIC_DRAW);
        
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, sel_buffer2)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 8, sel_buffer2)
        glBufferData(GL_SHADER_STORAGE_BUFFER, 5000*4, None , GL_DYNAMIC_DRAW);

        glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, counter_buffer)
        glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, counter_buffer)
        zero_array = np.array([0], dtype=np.int32)
        glBufferData(GL_ATOMIC_COUNTER_BUFFER, 4, zero_array , GL_DYNAMIC_DRAW);

#        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer)        
#        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.rpos_buffer);
        #glDispatchCompute(int(self.N/self.LOCALSIZEX)+1,1,1)        
        self.select_shader.run(self.N,1,1)        
        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)

        glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, counter_buffer)
        counter = glGetBufferSubData(GL_ATOMIC_COUNTER_BUFFER, 0, 4)
        counter = int.from_bytes(counter, "little")
        print("counter = ", counter)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 8, sel_buffer2)
        sel_data = glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, counter*4)
        selected_atoms2 = list(np.frombuffer(sel_data, dtype=np.int32))
        #print(selected_atoms)
        glUseProgram(0)
        sel_time_end = time.time()
        print(f"Selection time = {sel_time_end-sel_time_begin}")
        return selected_atoms2
