from ctypes import *
#from ctypes import Structure, c_float
import glm

class A(Structure):
    _fields_ = [
        ("c_pos",c_float*4)
    ]
    def __init__(self,):
        self.pos = glm.vec3(666, 666, 666)
        self.pos2 = glm.vec3(666, 0.2, 0.3)
    def to_ctypes(self):
        self.c_pos[0]=self.pos.x
        self.c_pos[0:3] = self.pos.to_list()
a = A()
a.to_ctypes()

print(bytearray(a))


from array import array
vert=[0.0,0.0,0.0,
      1.0,0.0,0.0,
      1.0,1.0,0.0,
      0.0,1.0,0.0]
ar=array("f",vert)
print(ar.tobytes())