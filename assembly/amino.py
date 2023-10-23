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
    if space.t==1:    #C + H
        a0 = Atom(x,y,z,3,r=10,m=12)
        space.appendatom(a0)
        a1 = Atom(x+50,y,z,1, f=pi)
        space.appendatom(a1)
        bond_atoms(a0,a1)
        space.atoms2compute()



    if space.t==500: #C+C+C
        space.compute2atoms()
        a2 = Atom(x,y+30,z,1)
        space.appendatom(a2)
        bond_atoms(space.atoms[0],a2)
        space.atoms2compute()

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
    space.update_delta = 10
    #space.gpu_compute.set(False)
    space.bondlock.set(True)
    App.run()
#
#
