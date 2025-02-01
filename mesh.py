import OpenGL.GL as gl
import OpenGL.GL.shaders
import ctypes
import glm

class Mesh():
    def __init__(self,vertices):
        self.vertices = vertices
        self.VAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.VAO )
        self.buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,self.buffer)
        stride = 4*6
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(0))
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, stride, ctypes.c_void_p(4*3))
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        # Send the data over to the buffer
        gl.glBufferData(gl.GL_ARRAY_BUFFER, 4*self.vertices.size, self.vertices, gl.GL_STATIC_DRAW)
        gl.glBindVertexArray( 0 )
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,0)
        pass

    def setShader(self,s):
        self.shader = s

    def bind(self):
        gl.glBindVertexArray(self.VAO)
        
    def draw(self):
        gl.glBindVertexArray(self.VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(self.vertices.size/6))
    
    def drawQuads(self):
        gl.glBindVertexArray(self.VAO)
        gl.glDrawArrays(gl.GL_QUADS, 0, int(self.vertices.size/6))

    def drawLines(self):
        gl.glBindVertexArray(self.VAO)
        gl.glDrawArrays(gl.GL_LINES, 0, int(self.vertices.size/6))
