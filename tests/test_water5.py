import random
import time
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm


f = 0
def action1(space):
    global f
    if space.t==1:    #OH
        random.seed(1)
        for i in range(0,200):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            x = random.randint(0,space.WIDTH)
            y = random.randint(0,space.HEIGHT)
            z = random.randint(0,space.DEPTH)        
            i=space.merge_from_file("examples/simple/H2O.json",x,y,z,rot)
        #space.merge_from_file("examples/alcohol/methanol.json",x,y,z)
        space.atoms2compute()
#            
# #
#
if __name__ == '__main__':
#
    App = mychemApp()
    space = App.space
    space.setSize(500,500,100)

    space.update_delta = 10
    space.REPULSION_KOEFF2 = 20.0
    space.INTERACT_KOEFF = 0.5
    space.action = action1
    #space.MASS_KOEFF = 5
    #space.NEARDIST=100
    #space.tranparentmode= True
     #space.recording = True
    #space.appendmixer(1)
    #space.redox.set(True)
    #space.highlight_unbond.set(True)
    space.pause = True
    App.run()
#
#
#300 - 9 fps
#300 - 1delta 40 fps
#2000 - 1delta 14,34 
#2000 - 5 delta 3,89
#2000 - 5 delta 29 fps  6000 atoms
#2000 - 10 delta 20 fps 6000 atoms