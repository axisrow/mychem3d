import OpenGL.GL as gl
import OpenGL.GL.shaders
import glfw
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


class AppOgl(OpenGLFrame):
    def set_space(self,space):
        self.space = space
    def initgl(self):
        """Initalize gl states when the frame is created"""
        gl.glViewport(0, 0, self.width, self.height)
        gl.glClearColor(0.2, 0.2, 0.2, 0.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable(gl.GL_DEBUG_OUTPUT)
        #gl.glEnable(gl.GL_CULL_FACE); 
        #gl.glEnable(gl.GL_FRAMEBUFFER_SRGB);
        #gl.glEnable(gl.GL_DEPTH_TEST)
        vertex_shader = open("shaders/atom_vertex1.glsl","r").read()
        fragment_shader = open("shaders/atom_frag1.glsl","r").read()
        compute_shader = open("shaders/space.glsl","r").read()
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
   
        self.pause = False
        self.cameraUp = glm.vec3(0,1,0)
        self.cameraFront = glm.vec3(0.5,0.5,-1)
        self.cameraPos = glm.vec3(0.5,0.5,1)
        self.cameraTarget = glm.vec3(0.5,0.5,0.5)

        #self.cameraDirection = glm.normalize(self.cameraPos - self.cameraTarget)
        self.keypressed = []
        self.lastframe_time= time.time()
        self.lastX = 500
        self.lastY = 300
        self.yaw = -90
        self.pitch = 0 
        self.fov = 50
        self.light_pos = glm.vec3(1.2,1.0,2.0)

        self.factor = 0.001

        self.sphere_vertices = np.array(make_sphere_vert(1,20), dtype=np.float32)
        self.cube_vertices = np.array(make_cube2(), dtype=np.float32)
        #cameraRight = glm.normalize(glm.cross(up, cameraDirection))
        #cameraUp = glm.cross(cameraDirection, cameraRight)
        self.create_objects()
        self.start = time.time()
        self.nframes = 0          


    def sphere2ssbo(self):  
        gl.glBindVertexArray(self.atomVAO )
        sp_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, sp_buffer)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, sp_buffer);
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, self.sphere_vertices.size*4, self.sphere_vertices , gl.GL_STATIC_DRAW);
        gl.glBindVertexArray(0 )


    def atoms2ssbo(self,bind_flag=True):
        if bind_flag: gl.glBindVertexArray(self.atomVAO )
        if len(self.space.atoms) >0:
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
                # a
                a_data.append(a.a.x)
                a_data.append(a.a.y)
                a_data.append(a.a.z)
                a_data.append(0.0)
                # type
                a_data.append(a.type)
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
        print(len(a_data))
        self.atoms_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.atoms_buffer)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer);
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, a_data.size*4, a_data , gl.GL_DYNAMIC_DRAW);

        self.atoms_buffer2 = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.atoms_buffer2)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.atoms_buffer2);
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, a_data.size*4, a_data , gl.GL_DYNAMIC_DRAW);
        if bind_flag: gl.glBindVertexArray(0)




    def create_objects(self):
        # create atom
        # Create a new VAO (Vertex Array Object) and bind it
        self.atomVAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.atomVAO )
        self.atoms2ssbo(bind_flag=False)

        # Generate buffers to hold our vertices
        sphere_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,sphere_buffer)

        stride = 4*6
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(0))
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(4*3))
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        # Send the data over to the buffer
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 4*self.sphere_vertices.size, self.sphere_vertices, gl.GL_STATIC_DRAW)
        gl.glBindVertexArray( 0 )
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,0)

        #create container
        self.ContainerVAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.ContainerVAO )
        container_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,container_buffer)
        stride = 4*3
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(0))
        #gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(4*3))
        gl.glEnableVertexAttribArray(0)
        #gl.glEnableVertexAttribArray(1)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 4*self.cube_vertices.size, self.cube_vertices, gl.GL_STATIC_DRAW)
        gl.glBindVertexArray(0)

        #create line
        self.lineVAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.lineVAO )
        line_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, line_buffer)
        stride=4*6
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(0))
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(4*3))
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        line_vertices = np.array([ 0.0, 0.0, 0.0,  0.0,0.0,-1.0, 1.0,0.0,0.0, 0.0,0.0,-1.0 ], dtype=np.float32)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 4*line_vertices.size, line_vertices, gl.GL_STATIC_DRAW)
        gl.glBindVertexArray(0)


#        self.lightVAO = gl.glGenVertexArrays(1)
#        gl.glBindVertexArray(self.lightVAO )
#        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,vertex_buffer)

#        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(0))
#        gl.glEnableVertexAttribArray(0)
#        gl.glBindVertexArray( 0 )
        
        # Unbind the VAO first (Important)
        
        # Unbind other stuff
        #gl.glDisableVertexAttribArray(position)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    
    
    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )
       
        gl.glUseProgram(self.shader)
        #camX = math.cos(self.nframes/500)*radius
        #camZ = math.sin(self.nframes/500)*radius
        #cameraPos = glm.vec3(camX,3, camZ)
        front = ( cos(glm.radians(self.pitch))*cos(glm.radians(self.yaw)),
                 sin(glm.radians(self.pitch)),
                 cos(glm.radians(self.pitch))*sin(glm.radians(self.yaw)),
                )
        #self.cameraDirection = glm.normalize(self.cameraPos - self.cameraTarget)
        self.cameraFront = glm.normalize(front)
        self.view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        #view = glm.translate(glm.vec3(0,5,-5))
        #view = view * glm.rotate(glm.radians(-55), glm.vec3(1,0,0)) 
        self.projection = glm.perspective(glm.radians(self.fov), self.width/self.height, 0.01,1000.0)
        #rmat = rotation_matrix((0,1,1), );
        model_loc = gl.glGetUniformLocation(self.shader, "model")
        view_loc = gl.glGetUniformLocation(self.shader, "view")
        proj_loc = gl.glGetUniformLocation(self.shader, "projection")
        mode_loc = gl.glGetUniformLocation(self.shader, "mode")
        gl.glUniformMatrix4fv(view_loc,1, gl.GL_FALSE, glm.value_ptr(self.view))
        gl.glUniformMatrix4fv(proj_loc,1, gl.GL_FALSE, glm.value_ptr(self.projection))
        objcol_loc = gl.glGetUniformLocation(self.shader, "objectColor")
        #light_loc = gl.glGetUniformLocation(self.shader, "lightColor")

        gl.glBindVertexArray(self.atomVAO)
        #render merge_atom
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        for a in self.space.merge_atoms:
            pos = glm.vec3(a.x, a.y, a.z)
            pos -= self.space.merge_center
            pos = self.space.merge_rot * pos
            pos += self.space.merge_center
            pos += self.space.merge_pos
            pos *= self.factor
            
            model =  glm.translate(pos)
            model =  glm.scale(model,glm.vec3(1)*self.factor*a.r)
            gl.glUniform3f(objcol_loc,a.color[0],a.color[1],a.color[2])
            gl.glUniformMatrix4fv(model_loc,1, gl.GL_FALSE, glm.value_ptr(model))
            #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(a.color)))
            #print(a.color)
             #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(1,0,0)))
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/3))

            #render merge atoms nodes
            for n in a.nodes:
                r1 = glm.quat(glm.vec3(0,-n.f2,n.f)) * glm.vec3(a.r,0,0)
                pos = a.rot * r1
                pos += glm.vec3(a.x,a.y,a.z)
                pos -= self.space.merge_center
                pos = self.space.merge_rot * pos
                pos += self.space.merge_center
                pos += self.space.merge_pos
                pos *= self.factor
                model =  glm.translate(pos)
                model =  glm.scale(model,glm.vec3(1)*self.factor*0.1*a.r)
                if n.bonded:
                    gl.glUniform3f(objcol_loc,0.0,1.0,0.0)
                else:
                    gl.glUniform3f(objcol_loc,1.0,1.0,1.0)
                gl.glUniformMatrix4fv(model_loc,1, gl.GL_FALSE, glm.value_ptr(model))
                #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(a.color)))
                #print(a.color)
                #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(1,0,0)))
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/3))
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        gl.glUniform1i(mode_loc,1)
        gl.glDrawArraysInstanced(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/3), len(self.space.atoms))
        #render_gl()
        #render np_atoms        
        # for i in range(0,self.space.np_x.size):
        #     a = self.space.atoms[i]
        #     pos = glm.vec3(self.space.np_x[i], self.space.np_y[i], self.space.np_z[i])
        #     pos *= self.factor
        #     model =  glm.translate(pos)
        #     model =  glm.scale(model,glm.vec3(1)*self.factor*a.r)
        #     gl.glUniform3f(objcol_loc,a.color[0],a.color[1],a.color[2])
        #     gl.glUniformMatrix4fv(model_loc,1, gl.GL_FALSE, glm.value_ptr(model))
        #     #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(a.color)))
        #     #print(a.color)
        #      #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(1,0,0)))
        #     gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/3))

        #     #render nodes
        #     for n in a.nodes:
        #         r1 = glm.quat(glm.vec3(0,-n.f2,n.f)) * glm.vec3(a.r,0,0)
        #         pos = self.space.np_rot[int(i)] * r1
        #         pos += glm.vec3(self.space.np_x[i], self.space.np_y[i],self.space.np_z[i])
        #         pos *= self.factor
        #         model =  glm.translate(pos)
        #         model =  glm.scale(model,glm.vec3(1)*self.factor*0.1*a.r)
        #         if n.bonded:
        #             gl.glUniform3f(objcol_loc,0.0,1.0,0.0)
        #         else:
        #             gl.glUniform3f(objcol_loc,1.0,1.0,1.0)
        #         gl.glUniformMatrix4fv(model_loc,1, gl.GL_FALSE, glm.value_ptr(model))
        #         #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(a.color)))
        #         #print(a.color)
        #         #gl.glUniform3fv(objcol_loc,1,glm.value_ptr(glm.vec3(1,0,0)))
        #         gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/3))

        gl.glUniform1i(mode_loc,0)
        gl.glBindVertexArray( 0 )

        # draw container            
        gl.glBindVertexArray(self.ContainerVAO)
        gl.glUniform3f(objcol_loc,1.0,1.0,1.0)
        #model =  glm.translate()
        model =  glm.mat4()
        model =  glm.translate(model, glm.vec3(0.5, 0.5,0.5))
        model =  glm.scale(model, glm.vec3(0.5,0.5,0.5))
        #model =  glm.scale(model,glm.vec3(1))
        gl.glUniformMatrix4fv(model_loc,1, gl.GL_FALSE, glm.value_ptr(model))
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE );
        gl.glDrawArrays(gl.GL_QUADS, 0, int(self.cube_vertices.size))
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL );
        gl.glBindVertexArray( 0 )

        #render selector
        if self.space.select_mode:
            gl.glBindVertexArray(self.atomVAO)
            #Установка цвета линии
            gl.glUniform3f(objcol_loc,1.0,0.0,0.0)
            if len(self.space.np_x)>0:
                model =  glm.mat4()
                pos = glm.vec3(self.space.np_x[self.space.select_i],self.space.np_y[self.space.select_i],self.space.np_z[self.space.select_i])
                model =  glm.translate(model, pos * self.factor  )
                model =  glm.scale(model, glm.vec3(0.01,0.01,0.01))
                gl.glUniformMatrix4fv(model_loc,1, gl.GL_FALSE, glm.value_ptr(model))
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE );
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(self.sphere_vertices.size/3))
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL );

                # Нарисовать линию между двумя точками
                #    gl.glDrawArrays(gl.GL_LINES, 0, 2)
        gl.glUseProgram(0)

        # render computed atoms
        
        #for i in range(1,10):
        if not self.pause:
            gl.glUseProgram(self.gpu_code)
            #gl.glBindVertexArray(self.atomVAO)

            gl.glDispatchCompute(100,1,1)        
            gl.glMemoryBarrier(gl.GL_SHADER_STORAGE_BARRIER_BIT);
        
            self.atoms_buffer,self.atoms_buffer2 = self.atoms_buffer2,self.atoms_buffer
            gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.atoms_buffer)
            gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.atoms_buffer2)
            gl.glUseProgram(0)
        #glfw.swap_buffers(self.);
        #glfwPollEvents();


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
#        if not self.pause:
#            for i in range(1,1):
#                n = self.space.compute()
        self.render()
        self.curframe_time = time.time()
        self.framedelta = self.curframe_time - self.lastframe_time 
   #     self.do_movement()
        #time.sleep(0.1)
        self.lastframe_time = self.curframe_time
        tm = time.time() - self.start
        throttle = 1/100 - self.framedelta
        #if throttle>0:
            #time.sleep(throttle)
        self.nframes += 1
        print("fps",self.nframes / tm, end="\r" )
