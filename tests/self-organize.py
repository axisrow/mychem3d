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
#
    for i in range(0,300):
        x = random.randint(50,950)
        y = random.randint(50,950)
        z = random.randint(50,950)
        f = glm.radians(random.randint(0,360))
        rot = glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random()))
        rot = glm.normalize(rot)
        space.merge_from_file("examples/aldehyde/formaldehyde.json",x,y,z,rot)
    space.update_delta = 5
     #space.recording = True
    #space.appendmixer(1)
    #space.redox.set(True)
    App.run()
#
#
#300 - 9 fps  update_delta=5    nodesinter 100


