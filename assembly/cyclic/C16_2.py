#!/usr/bin/python3.9
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




counter1 = 0

def action1(space):
    global a0,a1,a2,a3,a4,a5, counter1
    (x,y,z)=(400,500,990)
    if space.t==1:    #C+C
        space.BOND_KOEFF = 0.3
        for i in range(0,8):
            a = Atom(x+i*40,y,z,4)
            space.appendatom(a)
        for i in range(0,8):
            a = Atom(x+i*40,y+40,z,4)
            space.appendatom(a)
        space.atoms2compute()
        counter1 = 0


    if space.t==200+counter1*600: #C+C+C
        space.compute2atoms()
        bond_atoms(space.atoms[counter1], space.atoms[counter1+8])
        space.atoms2compute()
        
    if space.t==400+counter1*600: #C+C+C
        space.compute2atoms()
        bond_atoms(space.atoms[counter1], space.atoms[counter1+8])
        space.atoms2compute()

    if space.t==600+counter1*600: #C+C+C
        space.compute2atoms()
        bond_atoms(space.atoms[counter1], space.atoms[counter1+8],3)
        space.atoms2compute()
        if counter1<7: counter1+=1
        else: counter1=0


    if space.t==5000+counter1*400: #C+C
        space.compute2atoms()
        bond_atoms(space.atoms[counter1*2], space.atoms[counter1*2+1])
        space.atoms2compute()
        if counter1<3: counter1+=1
        else: counter1=0
        pass
    
    if space.t==6500: #C+C
        space.compute2atoms()
        bond_atoms(space.atoms[9], space.atoms[10])
        space.atoms2compute()

    if space.t==7800: #C+C
        space.compute2atoms()
        bond_atoms(space.atoms[13], space.atoms[14])
        space.atoms2compute()

    if space.t==9200: #C+C
        space.compute2atoms()
        bond_atoms(space.atoms[11], space.atoms[12])
        space.atoms2compute()


    if space.t==10000: #C+C
        space.compute2atoms()
        bond_atoms(space.atoms[8], space.atoms[15])
        #space.BOND_KOEFF=0.2
        #space.INTERACT_KOEFF=1
        space.atoms2compute()

    if space.t>10300 and space.t<10700: #C+C
        space.compute2atoms()
        space.atoms[11].v.y=-0.1
        space.atoms[12].v.y=-0.1
        space.atoms[8].v.y=0.1
        space.atoms[15].v.y=0.1
    #        space.atoms[11].v.y=-0.1
        space.atoms2compute()


    if space.t>10700 and space.t<11300: #C+C
        space.compute2atoms()
        space.atoms[8].v.x=+0.1
        space.atoms[15].v.x=-0.1
    #        space.atoms[11].v.y=-0.1
        space.atoms2compute()


    
############




    if space.t==50:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.5
    #space.BOND_KOEFF = 0.2
    space.REPULSION_KOEFF1 = 7
    space.REPULSION_KOEFF2 = 0
    space.update_delta = 40
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
