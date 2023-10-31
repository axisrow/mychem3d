import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm

    
def makelines(space,y):
     k = 0
     for i in range(100,900,13):
          for j in range(200,900,100):
               if k%2==0:
                    a = Atom(i,y,j,2,m=16,r=8)
                    f = glm.radians(40)
                    a.rot = glm.quat(cos(f/2), glm.vec3(0,0,1)* sin(f/2))
               else:
                    a = Atom(i,y+11,j,2,m=16,r=8)
                    f = glm.radians(40+180)
                    a.rot = glm.quat(cos(f/2), glm.vec3(0,0,1)* sin(f/2))
               a.calc_node_positions()
               space.appendatom(a)
          k+=1

#            
#
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    #makeplane(space,400)
    makelines(space,500)

    #a = Atom(500,700,500,100,m=100,r=50)
    #a.v = glm.vec3(0,-1,0)
    #space.appendatom(a)
    
    space.appendmixer(2)
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
