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
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    #makeplane(space,400)
   
    a = Atom(500,500,500,1)
    #a.v = glm.vec3(0,-1,0)
    space.appendatom(a)
    
    #space.appendmixer(2)
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
