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
    space.setSize(2000,200,1000)
    for i in range(0,300):
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)
        space.merge_from_file("examples/simple/NH3.json",x,y,z,rot)
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)
        space.merge_from_file("examples/aldehyde/glycolaldehyde.json",x,y,z,rot)

    space.update_delta = 5
     #space.recording = True
    #space.INTERACT_KOEFF = 1
    space.appendmixer(1)
    space.redox.set(True)
    App.run()
#
#
#300 - 9 fps  update_delta=5    nodesinter 100
#300 - 40 fps update_delta=5    nodesinter 40  near field 200, <5000 atoms
#300 - 26 fps update_delta=5    nodesinter 40  near field 300, <5000 atoms
#300 - 26 fps update_delta=5    nodesinter 40  near field 300, <`0000 atoms

