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
    global a0,a1,a2,a3,a4,a5,a6,a7,a8
    (x,y,z)=(500,500,500)
    if space.t==1:    #C+C
        a0 = Atom(x+20,y+40,z,3)
        space.appendatom(a0)
        a1 = Atom(x+40,y+20,z,4)
        space.appendatom(a1)
        a2 = Atom(x+40,y-20,z,3)
        space.appendatom(a2)
        a3 = Atom(x,y-40,z,4)
        space.appendatom(a3)
        a4 = Atom(x-40,y-20,z,4)
        space.appendatom(a4)
        a5 = Atom(x-40,y+20,z,4)
        space.appendatom(a5)
        a8 = Atom(x-70,y-30,z,3)
        space.appendatom(a8)
        a7 = Atom(x-70,y-55,z,4)
        space.appendatom(a7)
        a6 = Atom(x-70,y-85,z,3)
        space.appendatom(a6)




        bond_atoms(a0,a5,1,0)  #N+C
        space.atoms2compute()

    if space.t==200: #N+C 2
        space.compute2atoms()
        bond_atoms(a0,a5,0,2)
        space.atoms2compute()

    if space.t==400: #N+C
        space.compute2atoms()
        bond_atoms(a1,a2,0,0)
        space.atoms2compute()

    if space.t==600: #
        space.compute2atoms()
        bond_atoms(a1,a2,1,2)
        space.atoms2compute()


    if space.t==800: #
        space.compute2atoms()
        bond_atoms(a3,a4,0,0)
        space.atoms2compute()


    if space.t==1000: #
        space.compute2atoms()
        bond_atoms(a3,a4,1,2)
        space.atoms2compute()

############
    if space.t==1200: #C+C
        space.compute2atoms()
        bond_atoms(a0,a1)
        space.atoms2compute()


    if space.t==1500: #C+C
        space.compute2atoms()
        bond_atoms(a2,a3)
        space.atoms2compute()


    if space.t==1800: #C+C
        space.compute2atoms()
        bond_atoms(a4,a5)
        space.atoms2compute()


    if space.t==2200: #C+H
        space.compute2atoms()
        a = Atom(x+60,y+60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a1,a)
        space.atoms2compute()


    if space.t==2400: #C+H
        space.compute2atoms()
#        a = Atom(x+60,y-60,z,1,f=pi)
#        space.appendatom(a)
#        bond_atoms(a3,a)
        space.atoms2compute()

    if space.t==2600: #C+H
        space.compute2atoms()
#        a = Atom(x-60,y-60,z,1)
#        space.appendatom(a)
#        bond_atoms(a4,a)
        space.atoms2compute()


    if space.t==2800: #C+H
        space.compute2atoms()
        a = Atom(x-60,y+60,z,1)
        space.appendatom(a)
        bond_atoms(a5,a)
        space.atoms2compute()


    if space.t==3000: #C
        space.compute2atoms()
        bond_atoms(a6,a7)
        space.atoms2compute()


    if space.t==3200: #C
        space.compute2atoms()
        bond_atoms(a6,a7)
        space.atoms2compute()


    if space.t==3400: #C
        space.compute2atoms()
        bond_atoms(a7,a8)
        space.atoms2compute()

#####

    if space.t==3600: #C
        space.compute2atoms()
        bond_atoms(a3,a8)
        space.atoms2compute()

    if space.t==4400: #C
        space.compute2atoms()
        bond_atoms(a4,a6)
        space.atoms2compute()


    if space.t==5200: #C+H
        space.compute2atoms()
        a = Atom(x-60,y-60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a7,a)
        space.atoms2compute()


    if space.t==5400: #C+H
        space.compute2atoms()
        a = Atom(x-60,y-60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a8,a)
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
    #space.BONDS_KOEFF = 0.5
    space.REPULSION_KOEFF1 = 7
    space.update_delta = 15
    #space.gpu_compute.set(False)
    space.bondlock.set(True)
    App.run()
#
#
