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
    global a1,a2
    (x,y,z)=(500,500,500)
    if space.t==1:    # methyl + methyl
        #i0 = space.merge_from_file("examples/simple/methyl.json",0,0,0)
        a1 = Atom(x,y,z,5)
        space.appendatom(a1)
        a2 = Atom(x+50,y,z+50,2,f=pi,f2=pi/2)
        space.appendatom(a2)
        bond_atoms(a2,a1,0,3)
        bond_atoms(a2,a1,1,0)
        space.atoms2compute()

    if space.t==700:
        space.compute2atoms()
        #rot = glm.quat(cos(-pi/4), sin(-pi/4)*glm.vec3(0,0,1))  * glm.quat(cos(pi/4), sin(pi/4)*glm.vec3(1,0,0)) 
        i = space.merge_from_file("examples/simple/OH.json",-80,-30,0 )        
        bond_atoms(a1,space.atoms[i])
        space.atoms2compute()

    if space.t==1200:
        space.compute2atoms()
        i = space.merge_from_file("examples/simple/OH.json",40,-30,0 )        
        bond_atoms(a1,space.atoms[i])
        space.atoms2compute()


    if space.t==1600:
        space.compute2atoms()
        i = space.merge_from_file("examples/simple/OH.json",40,30,40 )        
        bond_atoms(a1,space.atoms[i])
        space.atoms2compute()




    if space.t==50:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    space.INTERACT_KOEFF = 0.5
    #space.REPULSION_KOEFF1 = 2
    #space.REPULSION_KOEFF2 = 0.01
    space.update_delta = 5
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
