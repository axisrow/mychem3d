import glm
from math import *

e = glm.quat()
f = glm.radians(360)
f2 = glm.radians(900000)
#r1 = glm.quat(cos(f/2), sin(f/2)*glm.vec3(0,0,1))
#r2 = glm.quat(cos(f2/2), sin(f2/2)*glm.vec3(0,1,0))
rot1 = glm.quat(glm.vec3(0,0,f))
#rot2 = glm.conjugate(rot1)
rot3 = glm.quat(1,glm.vec3(-1,-1,-1))*rot1
v = glm.vec3(1,0,0)
for i in range(0,1000000):
    v = rot1*v;
    #v = glm.normalize(rot1*v);
print(v)




