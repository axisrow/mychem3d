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
    (x,y,z)=(500,500,500)
    if space.t==1:    #C+C
        a0 = Atom(x,y,z,4,r=10,m=12)
        space.appendatom(a0)
        a1 = Atom(x+50,y,z,4)
        space.appendatom(a1)
        bond_atoms(a0,a1)
        space.atoms2compute()



    if space.t==450: #C+C+C
        space.compute2atoms()
        a2 = Atom(x,y,z+50,4,f2=-pi/2)
        space.appendatom(a2)
        bond_atoms(space.atoms[1],a2)
        space.atoms2compute()

    if space.t==1200:  # cycle
        space.compute2atoms()
        bond_atoms(space.atoms[0], space.atoms[2], ni2=2)
        space.atoms2compute()

    if space.t==2000: # C1 + H
        space.compute2atoms()
        a = Atom(x+20,y,z-10,1, f=pi)
        space.appendatom(a)
        bond_atoms(space.atoms[1], a)
        space.atoms2compute()

    if space.t==3200:  #C1 +H
        space.compute2atoms()
        a = Atom(x+40,y,z,1, f=pi)
        space.appendatom(a)
        bond_atoms(space.atoms[1],a)
        space.atoms2compute()

    if space.t==4000: # C0+H
        space.compute2atoms()
        a = Atom(x-20,y-20,z,1)
        space.appendatom(a)
        bond_atoms(space.atoms[0],a)
        space.atoms2compute()

    if space.t==4500: # C0+H
        space.compute2atoms()
        a = Atom(x+30,y+30,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(space.atoms[0],a)
        space.atoms2compute()


    if space.t==5000: # C2+H
        space.compute2atoms()
        a = Atom(x-30,y,z,1)
        space.appendatom(a)
        bond_atoms(space.atoms[2],a)
        space.atoms2compute()

    if space.t==5700: # C2+H
        space.compute2atoms()
        a = Atom(x,y,z+50,1)
        space.appendatom(a)
        bond_atoms(space.atoms[2],a)
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
