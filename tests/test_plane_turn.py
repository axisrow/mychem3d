import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm

    
def makeplane(space,y):
     for i in range(100,900,21):
          for j in range(200,900,21):
               a = Atom(i,y,j,400,m=12,r=10)
               a.rot = glm.quat(cos(pi/2.0/2.0), glm.vec3(1,0,0)* sin(pi/2.0/2.0))
               a.calc_node_positions()
               if j==200:
                    a.nodes[3].q=1
               if j>=893:
                    a.nodes[1].q=-1
               space.appendatom(a)

#            
#
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    #makeplane(space,400)
    makeplane(space,500)

    #a = Atom(500,700,500,100,m=100,r=50)
    #a.v = glm.vec3(0,-1,0)
    
    #space.appendmixer(2)
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
