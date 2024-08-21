import glm
from math import *

cameraUp = glm.vec3(0,1,0)
cameraFront = glm.vec3(0.5,0.5,-1)
cameraPos = glm.vec3(0.5,0.5,2)
        #self.cameraPos = glm.vec3(0.5,0.5,0.5)
cameraTarget = glm.vec3(0.5,0.5,0.5)

yaw = -90
pitch = 0 
fov = 45

front = ( cos(glm.radians(pitch))*cos(glm.radians(yaw)),
                 sin(glm.radians(pitch)),
                 cos(glm.radians(pitch))*sin(glm.radians(yaw)),
                )
cameraFront = glm.normalize(front)
view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
width = 1024
height = 600
projection = glm.perspective(glm.radians(fov), width/height, 0.01,10.0)

print('camfront', cameraFront)
print("view", view)

pos = glm.vec4(0.0,0.0,10.0,1.0)
print(view*pos)
print(projection*(view*pos))



