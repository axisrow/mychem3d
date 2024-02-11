import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm

#            
# #
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(1000,1000,300)
    for i in range(0,20):
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)        
        i1 = space.merge_from_file("examples/carboxylic/capric_acid.json",x,y,z,rot)
        #space.merge_from_file("examples/alcohol/methanol.json",x,y,z)
    for i in range(0,3000):
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)        
        i2 = space.merge_from_file("examples/simple/H2O.json",x,y,z,rot)
        #space.merge_from_file("examples/alcohol/methanol.json",x,y,z)

    space.update_delta = 5
    space.INTERACT_KOEFF = 0.4
     #space.recording = True
    #space.appendmixer(1)
    #space.redox.set(True)
    App.run()
#
#
#300 - 9 fps
#300 - 1delta 40 fps
#2000 - 1delta 14,34 
#2000 - 5 delta 3,89