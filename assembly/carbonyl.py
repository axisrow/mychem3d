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
    if space.t==1:    #C + O
        a0 = Atom(x,y,z,4,r=10,m=12)
        space.appendatom(a0)
        a1 = Atom(x+50,y,z,2,f=4*pi/5,f2=3*pi/4)
        space.appendatom(a1)
        bond_atoms(a0,a1)
        bond_atoms(a0,a1)
        space.atoms2compute()



    if space.t==500: #
        space.compute2atoms()
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
    space.update_delta = 10
    #space.gpu_compute.set(False)
    space.bondlock.set(True)
    App.run()
#
#
