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
        (x,y,z)=(20,20,20)
        for i in range(0,700):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            x+=40
            if x>450: 
                y+=40
                x=20
            if y>450:
                z+=40
                y=20
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
    space.setSize(600,600,500)

    space.update_delta = 10
    space.REPULSION_KOEFF2 = 350.0
    space.INTERACT_KOEFF = 5
    space.BOND_KOEFF = 0.3
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