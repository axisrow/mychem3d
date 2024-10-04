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


def action1(space:Space):
    
    if space.t==1:    # methyl + methyl
        space.compute2atoms()
        i0 = space.merge_from_file("examples/2d/aldehyde/acetaldehyde.json",0,0,50)
        a1 = Atom(500,500,500,400)
        a2 = Atom(525,505,500,200)
        space.appendatom(a1)
        space.appendatom(a2)
        a1.nodes[1].q=-1
        #rot = glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
        #rot = glm.quat(0, 0, 0, 1)
        #i1 = space.merge_from_file("examples/simple/methyl.json",-60,-30,0,rot )
        #bond_atoms(a1,a2,2)
        space.atoms2compute()
#    if space.t==3:
#        space.pause = True





    if space.t==50:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.1
    space.update_delta = 15
    space.REPULSION_KOEFF1 = 10
    #space.REPULSION_KOEFF2 = 1
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
