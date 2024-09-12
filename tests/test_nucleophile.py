import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from mychem_functions import bond_atoms
from math import pi 
import mychem3d
from math import *
import glm


f = 0
def action1(space:Space):
    global f,c1,c2,c3,c4,n1,n2,n3,n4,o1,o2,o3,o4
#    (x,y,z)=(300,300,300)
    if space.t==1:    #OH
        for i in range(0,30):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            x = random.randint(0,space.WIDTH)
            y = random.randint(0,space.HEIGHT)
            z = random.randint(0,space.DEPTH)
            space.merge_from_file("examples/galogenides/MeCl.json",x,y,z,rot)
        for i in range(0,30):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            x = random.randint(0,space.WIDTH)
            y = random.randint(0,space.HEIGHT)
            z = random.randint(0,space.DEPTH)
            i=space.merge_from_file("examples/simple/OH.json",x,y,z,rot)
            space.atoms[i].nodes[1].q=-1

        space.atoms2compute()    
        





if __name__ == '__main__':
#
    App = mychemApp()
    space = App.space
    space.setSize(500,500,500)
    space.action = action1
    #space.INTERACT_KOEFF = 0.4
    #space.BOND_KOEFF = 0.15
    #space.ROTA_KOEFF = 1
    #space.REPULSION_KOEFF2=0.2
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)



    App.run()
#
#

