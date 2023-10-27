import OpenGL.GL as gl
import OpenGL.GL.shaders
#import glfw
import ctypes
from pyopengltk import OpenGLFrame
import numpy as np
import glm
import random
from PIL import Image
from math import sin,cos,sqrt,pi
import time
from mychem_functions import make_sphere_vert,make_cube2
from mychem_data import cube_vertices
from array import array
from mesh import Mesh

class AppOgl(OpenGLFrame):
    def set_space(self,space):
        self.space = space
    def initgl(self):
        """Initalize gl states when the frame is created"""
        print("init gl")
        gl.glViewport(0, 0, self.width, self.height)
        gl.glClearColor(0.3, 0.3, 0.3, 0.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable(gl.GL_CULL_FACE);
        #gl.glCullFace(gl.GL_FRONT); 
        #gl.glFrontFace(gl.GL_CW) 
        #gl.glEnable(gl.GL_DEBUG_OUTPUT)
        #gl.glEnable(gl.GL_CULL_FACE); 
        #gl.glEnable(gl.GL_FRAMEBUFFER_SRGB);
        #gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable (gl.GL_LINE_SMOOTH);    
        #gl.glfwWindowHint(gl.GLFW_SAMPLES, 4);
        #gl.glEnable(gl.GL_MULTISAMPLE); 
        

        vertex_shader = open("shaders/atom_vertex1.glsl","r").read()
        fragment_shader = open("shaders/atom_frag1.glsl","r").read()
        compute_shader = open("shaders/compute.glsl","r").read()
#        geom_shader = open("shaders/atom_geom1.glsl","r").read()

        self.shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
#            OpenGL.GL.shaders.compileShader(geom_shader, gl.GL_GEOMETRY_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER),validate=False
        )
        
        OpenGL.GL.shaders.compileShader(compute_shader, gl.GL_COMPUTE_SHADER)
        self.compute_shader = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
        gl.glShaderSource(self.compute_shader, compute_shader)
        gl.glCompileShader(self.compute_shader)
        
        self.gpu_code = gl.glCreateProgram()
        gl.glAttachShader(self.gpu_code, self.compute_shader)
        gl.glLinkProgram(self.gpu_code)
   
        self.cameraUp = glm.vec3(0,1,0)
        self.cameraFront = glm.vec3(0.5,0.5,-1)
        self.cameraPos = glm.vec3(0.5,0.5,1)
        #self.cameraPos = glm.vec3(0.5,0.5,0.5)
        self.cameraTarget = glm.vec3(0.5,0.5,0.5)

        #self.cameraDirection = glm.normalize(self.cameraPos - self.cameraTarget)
        self.keypressed = []
        self.lastframe_time= time.time()
        self.lastX = 500
        self.lastY = 300
        self.yaw = -90
        self.pitch = 0 
        self.fov = 45
        self.light_pos = glm.vec3(1.2,1.0,2.0)

        self.factor = 0.001

        self.sphere_vertices = np.array(make_sphere_vert(1,20), dtype=np.float32)
        self.sphere_vertices2 = np.array(make_sphere_vert(1,5), dtype=np.float32)
        self.cube_vertices = np.array(make_cube2(), dtype=np.float32)
        #np.array(make_cube2(), dtype=np.float32)
        #cameraRight = glm.normalize(glm.cross(up, cameraDirection))
        #cameraUp = glm.cross(cameraDirection, cameraRight)
        self.create_objects()
        print("objects created")
        self.space.atoms2compute()

        self.start = time.time()
        self.nframes = 0          
        self.rframes = 0
        self.initok = True



    def atoms2ssbo(self,bind_flag=True):
        self.N = len(self.space.atoms)
        print(f"Atoms2ssbo N={self.N}")
        #if bind_flag: gl.glBindVertexArray(self.atomMesh.VAO )
        if self.N>0:
            a_data = []
            for a in self.space.atoms:
                #
                a_data.append(a.pos.x)
                a_data.append(a.pos.y)
                a_data.append(a.pos.z)
                a_data.append(0.0)
                # v
                a_data.append(a.v.x)
                a_data.append(a.v.y)
                a_data.append(a.v.z)
                a_data.append(0.0)
                # type, radius, m
                a_data.append(a.type)
                a_data.append(a.r)
                a_data.append(a.m)
                a_data.append(len(a.nodes))
                #rot 
                a_data.append(a.rot.x)
                a_data.append(a.rot.y)
                a_data.append(a.rot.z)
                a_data.append(a.rot.w)
                #rotv 
                a_data.append(a.rotv.x)
                a_data.append(a.rotv.y)
                a_data.append(a.rotv.z)
                a_data.append(a.rotv.w)
                # q
                a_data.append(0)
                a_data.append(0)
                a_data.append(0)
                a_data.append(0)
                for n in a.nodes:
                    a_data.append(n.pos.x)
                    a_data.append(n.pos.y)
                    a_data.append(n.pos.z)
                    a_data.append(0.0)
                    a_data.append(n.q)
                    a_data.append(n.bonded)
                    a_data.append(n.pair)
                    a_data.append(0.0)
                for i in range(0,5-len(a.nodes)):
                    a_data.append(0.0)
                    a_data.append(0.0)
                    a_data.append(0.0)
                    a_data.append(0.0)
                    a_data.append(0.0)
                    a_data.append(0.0)
                    a_data.append(0.0)
                    a_data.append(0.0)
                #color
                a_data.append(a.color[0])
                a_data.append(a.color[1])
                a_data.append(a.color[2])
                a_data.append(1.0)


            a_data = np.array(a_data, dtype=np.float32)
        else:
            a_data = np.array([], dtype=np.float32)
        #print(a_data)
        print(f"atoms buffer len={len(a_data)}")
        self.atoms_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.atoms_buffer)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer);
        
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, a_data.size*4, a_data , gl.GL_DYNAMIC_DRAW);
        
        self.atoms_buffer2 = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.atoms_buffer2)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.atoms_buffer2);
        zero = np.zeros(a_data.size)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, zero.size*4, zero , gl.GL_DYNAMIC_DRAW);
        if bind_flag: gl.glBindVertexArray(0)


    def numpy2ssbo(self):
        self.N = len(self.space.atoms)
        if self.N==0: return
        #print(f"numpy2ssbo N={self.N}")
        space = self.space
        asize = 68
        a_data = np.empty([self.N*asize],dtype=np.float32)
        offset = 0
        for i in range(0,self.N):
            #
            a = self.space.atoms[i]
            a_data[offset]   = space.np_x[i]
            offset +=1
            a_data[offset] = space.np_y[i]
            offset +=1
            a_data[offset] = space.np_z[i]
            offset +=1
            a_data[offset] = 0.0
            offset +=1
            # v
            a_data[offset]=space.np_vx[i]
            offset +=1
            a_data[offset]=space.np_vy[i]
            offset +=1
            a_data[offset]=space.np_vz[i]
            offset +=1
            a_data[offset]=0.0
            offset +=1
            # type, radius, m
            a_data[offset]=a.type
            offset +=1
            a_data[offset]=a.r
            offset +=1
            a_data[offset]=a.m
            offset +=1
            a_data[offset]=len(a.nodes)
            offset +=1
            #rot 
            a_data[offset]=space.np_rot[i].x
            offset +=1
            a_data[offset]=space.np_rot[i].y
            offset +=1
            a_data[offset]=space.np_rot[i].z
            offset +=1
            a_data[offset]=space.np_rot[i].w
            offset +=1
            #rotv 
            a_data[offset]=space.np_rotv[i].x
            offset +=1
            a_data[offset]=space.np_rotv[i].y
            offset +=1
            a_data[offset]=space.np_rotv[i].z
            offset +=1
            a_data[offset]=space.np_rotv[i].w
            offset +=1
            # anim
            a_data[offset] =0.0
            offset +=1
            a_data[offset] =0.0
            offset +=1
            a_data[offset] =0.0
            offset +=1
            a_data[offset] =0.0
            offset +=1
            for n in a.nodes:
                a_data[offset]   = n.pos.x
                offset +=1
                a_data[offset] = n.pos.y
                offset +=1
                a_data[offset] = n.pos.z
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = n.q
                offset +=1
                a_data[offset] = n.bonded
                offset +=1
                a_data[offset] = -1.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
            for i in range(0,5-len(a.nodes)):
                a_data[offset]   = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
                a_data[offset] = 0.0
                offset +=1
            #color 
            a_data[offset]=a.color[0]
            offset +=1
            a_data[offset]=a.color[1]
            offset +=1
            a_data[offset]=a.color[2]
            offset +=1
            a_data[offset]=1.0
            offset +=1
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.atoms_buffer)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer);
        gl.glBufferSubData(gl.GL_SHADER_STORAGE_BUFFER, 0, a_data.size*4, a_data )

    def ssbo2atoms(self):
        self.N = len(self.space.atoms)
        print(f"ssbo2atoms N={self.N}")
        space = self.space
        asize = 68
        #a_data = np.empty([self.N*asize],dtype=np.float32)
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.atoms_buffer)
        #gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer);
        a_data8 = gl.glGetBufferSubData(gl.GL_SHADER_STORAGE_BUFFER, 0, self.N*asize*4)
        a_data = a_data8.view('<f4')
        #self.space.fdata.write(np.array2string(a_data)+" " + str(self.space.t)+"\n")
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        offset = 0
        for i in range(0,self.N):
            #
            a = self.space.atoms[i]
            a.pos.x = float(a_data[offset]) 
            offset +=1
            a.pos.y = float(a_data[offset])
            offset +=1
            a.pos.z = float(a_data[offset])
            offset +=1
            offset +=1
            # v
            a.v.x = float(a_data[offset])
            offset +=1
            a.v.y = float(a_data[offset])
            offset +=1
            a.v.z = float(a_data[offset])
            offset +=1
            offset +=1
            # type, radius, m
            #a_data[offset]=a.type
            offset +=1
            #a_data[offset]=a.r
            offset +=1
            #a_data[offset]=a.m
            offset +=1
            #a_data[offset]=len(a.nodes)
            offset +=1
            #rot 
            a.rot.x = float(a_data[offset])
            offset +=1
            a.rot.y = float(a_data[offset])
            offset +=1
            a.rot.z = float(a_data[offset])
            offset +=1
            a.rot.w = float(a_data[offset])
            offset +=1
            #rotv 
            a.rotv.x = float(a_data[offset])
            offset +=1
            a.rotv.y = float(a_data[offset])
            offset +=1
            a.rotv.z = float(a_data[offset])
            offset +=1
            a.rotv.w = float(a_data[offset])
            offset +=1
            # anim
            #a_data[offset] =0.0
            offset +=1
            #a_data[offset] =0.0
            offset +=1
            #a_data[offset] =0.0
            offset +=1
            #a_data[offset] =0.0
            offset +=1
            for n in a.nodes:
                #a_data[offset]   = n.pos.x
                offset +=1
                #a_data[offset] = n.pos.y
                offset +=1
                #a_data[offset] = n.pos.z
                offset +=1
                #a_data[offset] = 0.0
                offset +=1
                n.q = float(a_data[offset])
                offset +=1
                n.bonded = bool(a_data[offset])
                offset +=1
                n.pair = float(a_data[offset])
                offset +=1
                #a_data[offset] = 0.0
                offset +=1
            for i in range(0,5-len(a.nodes)):
                offset +=8
            #color 
            #a_data[offset]=a.color[0]
            offset +=1
            #a_data[offset]=a.color[1]
            offset +=1
            #a_data[offset]=a.color[2]
            offset +=1
            #a_data[offset]=1.0
            offset +=1


    def create_objects(self):
        print("create objects start")
        self.atomMesh = Mesh(self.sphere_vertices)
        self.atomMesh.setup()
        self.nodeMesh = Mesh(self.sphere_vertices2)
        self.nodeMesh.setup()
        self.containerMesh = Mesh(self.cube_vertices)
        self.containerMesh.setup()

    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )
       
        gl.glUseProgram(self.shader)
        front = ( cos(glm.radians(self.pitch))*cos(glm.radians(self.yaw)),
                 sin(glm.radians(self.pitch)),
                 cos(glm.radians(self.pitch))*sin(glm.radians(self.yaw)),
                )
        self.cameraFront = glm.normalize(front)
        self.view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        self.projection = glm.perspective(glm.radians(self.fov), self.width/self.height, 0.01,1000.0)
        model_loc = gl.glGetUniformLocation(self.shader, "model")
        view_loc = gl.glGetUniformLocation(self.shader, "view")
        proj_loc = gl.glGetUniformLocation(self.shader, "projection")
        mode_loc = gl.glGetUniformLocation(self.shader, "mode")
        nodeindex_loc = gl.glGetUniformLocation(self.shader, "nodeindex")
        gl.glUniformMatrix4fv(view_loc,1, gl.GL_FALSE, glm.value_ptr(self.view))
        gl.glUniformMatrix4fv(proj_loc,1, gl.GL_FALSE, glm.value_ptr(self.projection))
        objcol_loc = gl.glGetUniformLocation(self.shader, "objectColor")
        #light_loc = gl.glGetUniformLocation(self.shader, "lightColor")

        #render merge_atom
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        for a in self.space.merge_atoms:
            pos = glm.vec3(a.pos)
            pos -= self.space.merge_center
            pos = self.space.merge_rot * pos
            pos += self.space.merge_center
            pos += self.space.merge_pos
            pos *= self.factor
            model =  glm.translate(pos)
            model =  glm.scale(model,glm.vec3(1)*self.factor*a.r)
            self.atomMesh.modelmatrix = model
            self.atomMesh.color = a.color
            self.atomMesh.draw(self.shader)
            #render merge atoms nodes
            for n in a.nodes:
                pos = a.rot * n.pos
                pos += a.pos
                pos -= self.space.merge_center
                pos = self.space.merge_rot * pos
                pos += self.space.merge_center
                pos += self.space.merge_pos
                pos *= self.factor
                model =  glm.translate(pos)
                model =  glm.scale(model,glm.vec3(1)*self.factor*0.1*a.r)
                if n.bonded:
                     self.nodeMesh.color = (0.0,1.0,0.0) 
                else:
                     self.nodeMesh.color = (1.0,1.0,1.0) 
                self.nodeMesh.modelmatrix = model
                self.nodeMesh.draw(self.shader)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        #if self.space.gpu_compute.get():
        gl.glBindVertexArray(self.atomMesh.VAO )
        # render computed atoms
        gl.glUniform1i(mode_loc,1)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/6), len(self.space.atoms))

        gl.glUniform1i(mode_loc,2)
        gl.glBindVertexArray(self.nodeMesh.VAO )
        for i in range(0,5):
                gl.glUniform1i(nodeindex_loc,i)
                gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, int(self.sphere_vertices2.size/6), len(self.space.atoms))

        gl.glUniform1i(mode_loc,0)
        gl.glBindVertexArray( 0 )

        # draw container            
        model =  glm.mat4()
        model =  glm.translate(model, glm.vec3(0.5, 0.5,0.5))
        model =  glm.scale(model, glm.vec3(0.5,0.5,0.5))
        model =  glm.scale(model,glm.vec3(1))
        self.containerMesh.color = (1,1,1)
        self.containerMesh.modelmatrix = model
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE );
        self.containerMesh.drawQuads(self.shader)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL );
        
        #render selector
        if self.space.select_mode:
            if len(self.space.np_x)>0:
                model =  glm.mat4()
                pos = glm.vec3(self.space.np_x[self.space.select_i],self.space.np_y[self.space.select_i],self.space.np_z[self.space.select_i])
                model =  glm.translate(model, pos * self.factor  )
                model =  glm.scale(model, glm.vec3(0.01,0.01,0.01))
                self.atomMesh.color = (1,0,0)
                self.atomMesh.modelmatrix = model
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE );
                self.atomMesh.draw(self.shader)
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL );
        gl.glUseProgram(0)

        # gpu compute atoms
        gl.glBindVertexArray(self.atomMesh.VAO )
        if not self.space.pause and self.space.gpu_compute.get():
            gl.glUseProgram(self.gpu_code)
            self.loc = {}
            self.loc.update ( {"iTime": gl.glGetUniformLocation(self.gpu_code, "iTime")})
            bondloc_loc = gl.glGetUniformLocation(self.gpu_code, "bondlock")
            gravity_loc = gl.glGetUniformLocation(self.gpu_code, "gravity")
            redox_loc = gl.glGetUniformLocation(self.gpu_code, "redox")
            shk_loc = gl.glGetUniformLocation(self.gpu_code, "shake")
            bk_loc = gl.glGetUniformLocation(self.gpu_code, "BOND_KOEFF")
            ik_loc = gl.glGetUniformLocation(self.gpu_code, "INTERACT_KOEFF")
            rk1_loc = gl.glGetUniformLocation(self.gpu_code, "REPULSION_KOEFF1")
            rk2_loc = gl.glGetUniformLocation(self.gpu_code, "REPULSION_KOEFF2")
            rotk_loc = gl.glGetUniformLocation(self.gpu_code, "ROTA_KOEFF")
            gl.glUniform1i(bondloc_loc,self.space.bondlock.get())
            gl.glUniform1i(self.loc["iTime"],self.space.t)
            gl.glUniform1i(gravity_loc,self.space.gravity.get())
            gl.glUniform1i(redox_loc,self.space.redox.get())
            gl.glUniform1f(bk_loc,self.space.BOND_KOEFF)
            gl.glUniform1f(ik_loc,self.space.INTERACT_KOEFF)
            gl.glUniform1f(rk1_loc,self.space.REPULSION_KOEFF1)
            gl.glUniform1f(rk2_loc,self.space.REPULSION_KOEFF2)
            gl.glUniform1f(rotk_loc,self.space.ROTA_KOEFF)

            for i in range(0,self.space.update_delta):
                self.space.t+=1
                if not self.space.pause:
                    gl.glDispatchCompute(int(len(self.space.atoms)/50)+1,1,1)        
                    gl.glMemoryBarrier(gl.GL_SHADER_STORAGE_BARRIER_BIT)
                    self.atoms_buffer,self.atoms_buffer2 = self.atoms_buffer2,self.atoms_buffer
                    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer)
                    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.atoms_buffer2)
                    if self.space.action:
                        self.space.action(self.space)   
            gl.glUseProgram(0)


    def do_movement(self):
        cameraSpeed = 5 * self.framedelta
        if 'w' in self.keypressed:
              self.cameraPos += cameraSpeed * self.cameraFront
        if 's' in self.keypressed:
              self.cameraPos -= cameraSpeed * self.cameraFront
        if 'a' in self.keypressed:
              self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed
        if 'd' in self.keypressed:
              self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed


    def redraw(self):
        """Render a single frame"""
        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        if not self.space.pause and not self.space.gpu_compute.get():
            for i in range(0,self.space.update_delta):
                self.space.t+=1
                n = self.space.compute()
                self.numpy2ssbo()
        self.render()
        if self.space.recording.get() and not self.space.pause:
            pix = gl.glReadPixels(0,0,self.width, self.height,gl.GL_RGB,gl.GL_UNSIGNED_BYTE)
            img = Image.frombytes("RGB", (self.width,self.height), pix)
            img2 = img.transpose(method=Image.FLIP_TOP_BOTTOM)
            img2.save("output/frame"+str(self.rframes)+".png")
            self.rframes+=1


#        if self.nframes%50==0:
           
           
                            
        self.curframe_time = time.time()
        self.framedelta = self.curframe_time - self.lastframe_time 
   #     self.do_movement()
        #time.sleep(0.1)
        self.lastframe_time = self.curframe_time
        tm = time.time() - self.start
        throttle = 1/40 - self.framedelta
        if throttle>0:
            time.sleep(throttle)
        self.nframes += 1
                
#        print("fps",self.nframes / tm, end="\r" )
        if self.nframes%10 == 0:
            if self.framedelta!=0:
                self.status_bar.setFPS(1/self.framedelta)
