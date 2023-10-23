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


def action1(space):
    (x,y,z)=(500,500,500)
    if space.t==1:    # methyl + methyl
        i0 = space.merge_from_file("examples/simple/methyl.json",0,0,0)
        rot = glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
        #rot = glm.quat(0, 0, 0, 1)
        i1 = space.merge_from_file("examples/simple/methyl.json",-60,-30,0,rot )
        bond_atoms(space.atoms[i0],space.atoms[i1])
        space.atoms2compute()





    if space.t==50:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    space.INTERACT_KOEFF = 0.1
    space.update_delta = 15
    #space.gpu_compute.set(False)
    space.bondlock.set(True)
    App.run()
#
#
