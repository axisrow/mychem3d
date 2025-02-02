from OpenGL.GL import *
import numpy as np

class Buffer():
    def __init__ (self, buffertype=GL_SHADER_STORAGE_BUFFER):
        self.buffer = glGenBuffers(1)
        self.buffertype = buffertype

    def bind_to(self,n):
        glBindBuffer(self.buffertype, self.buffer)
        glBindBufferBase(self.buffertype, n, self.buffer);        


    def write(self, data):
        glBindBuffer(self.buffertype, self.buffer)
        glBufferData(self.buffertype, data.size, data , GL_DYNAMIC_DRAW)

    def zero(self, size):
        zero = np.zeros(size,dtype=np.byte)
        glBindBuffer(self.buffertype, self.buffer)
        glBufferData(self.buffertype, size, zero , GL_DYNAMIC_DRAW)

    def subread(self,size, offset=0):
        glBindBuffer(self.buffertype, self.buffer)
        return glGetBufferSubData(self.buffertype, offset, size)
