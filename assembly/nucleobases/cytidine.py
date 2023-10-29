import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from mychem3d import mychemApp, Atom,Space
from mychem_functions import bond_atoms
from math import pi 
import mychem3d
from math import *
import glm


def action1(space):
    global i0,i1,index
    (x,y,z)=(500,500,500)
    if space.t==1:    # methyl + methyl
        i0 = space.merge_from_file("examples/sugar/ribozaA.json",0,0,0)
        rot = glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
        i1 = space.merge_from_file("examples/nucleobase/cytosine.json",60,60,0)
        bond_atoms(space.atoms[i0],space.atoms[i1])
        #space.atoms[i0+1].color = (0,1,0)
        #space.atoms[i1+0].color = (0,1,0)
        space.atoms[i0+1].nodes[1].q=0
        space.atoms[i1].nodes[0].q=0
        space.atoms2compute()
        index = 0

    if space.t==300:
        space.compute2atoms()
        bond_atoms(space.atoms[i0+1],space.atoms[i1])
        space.atoms2compute()
        pass

    if space.t==1000:
        space.compute2atoms()
        space.atoms[6].color = (0,0,0)  #spec color for remove on save
        space.atoms[7].color = (0,0,0)
        space.atoms[26].color = (0,0,0)
        space.atoms2compute()

    # search water
    #if space.t>1 and space.t%200==0:
       #print(index)
       #space.compute2atoms()
       #space.atoms[index].color = (0,1,0)
       #index+=1
       #space.atoms2compute()
       #pass



if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.1
    space.update_delta = 5
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
