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
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)
        space.merge_from_file("examples/simple/NH3.json",x,y,z)
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)
        space.merge_from_file("examples/aldehyde/glycolaldehyde.json",x,y,z)

    space.update_delta = 5
     #space.recording = True
    #space.INTERACT_KOEFF = 1
    space.appendmixer(1)
    space.redox.set(True)
    App.run()
#
#
#300 - 9 fps  update_delta=5    nodesinter 100


