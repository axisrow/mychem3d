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
    global a0,a1,a2,a3,a4,a5
    (x,y,z)=(500,500,500)
    if space.t==1:    #C+C
        a0 = Atom(x,y+50,z,2)
        space.appendatom(a0)
        a1 = Atom(x+40,y+20,z,4)
        space.appendatom(a1)
        a2 = Atom(x+30,y-20,z,4)
        space.appendatom(a2)
        a3 = Atom(x-20,y-20,z,4)
        space.appendatom(a3)
        a4 = Atom(x-40,y+20,z,4)
        space.appendatom(a4)
        a5 = Atom(x-60,y+50,z,4)
        space.appendatom(a5)

        bond_atoms(a0,a1,1,0)
        space.atoms2compute()

    if space.t==200: #C+C+C
        space.compute2atoms()
        bond_atoms(a1,a2,3,1)
        space.atoms2compute()

    if space.t==600: #C+C+C
        space.compute2atoms()
        bond_atoms(a2,a3,2,1)
        space.atoms2compute()

    if space.t==900: #C+C
        space.compute2atoms()
        bond_atoms(a3,a4,0,0)
        space.atoms2compute()


    if space.t==1200: #C+C
        space.compute2atoms()
        bond_atoms(a4,a0)
        space.atoms2compute()


    if space.t==1500: #C+C
        space.compute2atoms()
        bond_atoms(a4,a5)
        space.atoms2compute()

############
    if space.t==1800: #C+C
        space.compute2atoms()
        rot = glm.quat(cos(pi/4), sin(pi/4)*glm.vec3(1,0,0))
        i = space.merge_from_file("examples/simple/OH.json",40,20,40,rot )        
        bond_atoms(a1,space.atoms[i])
        space.atoms2compute()


    if space.t==2300: #C+C
        space.compute2atoms()
        rot = glm.quat(cos(pi/4), sin(pi/4)*glm.vec3(1,0,0))
        i = space.merge_from_file("examples/simple/OH.json",20,20,-20,rot )        
        bond_atoms(a2,space.atoms[i],3)
        space.atoms2compute()


    if space.t==2600: #C+C
        space.compute2atoms()
        rot = glm.quat(cos(-pi/4), sin(-pi/4)*glm.vec3(0,0,1)) * glm.quat(cos(pi/4), sin(pi/4)*glm.vec3(1,0,0)) 
        i = space.merge_from_file("examples/simple/OH.json",0,-30,-20,rot )        
        bond_atoms(a3,space.atoms[i])
        space.atoms2compute()


    if space.t==2900: #C+C
        space.compute2atoms()
        rot = glm.quat(cos(-pi/4), sin(-pi/4)*glm.vec3(0,0,1))  * glm.quat(cos(pi/4), sin(pi/4)*glm.vec3(1,0,0)) 
        i = space.merge_from_file("examples/simple/OH.json",-80,-30,40,rot )        
        bond_atoms(a5,space.atoms[i],2)
        space.atoms2compute()
##########
    if space.t==3300: #C+C
        space.compute2atoms()
        a = Atom(x+70,y+60,z-30,1,f=pi)
        space.appendatom(a)
        bond_atoms(a1,a)
        space.atoms2compute()


    if space.t==3600: #C+C
        space.compute2atoms()
        a = Atom(x+70,y,z+30,1,f=pi)
        space.appendatom(a)       
        bond_atoms(a2,a)
        space.atoms2compute()


    if space.t==3900: #C+C
        space.compute2atoms()
        a = Atom(x,y+50,z+30,1,f=pi/2)
        space.appendatom(a)        
        bond_atoms(a3,a)
        space.atoms2compute()

    if space.t==4200: #C+C
        space.compute2atoms()
        a = Atom(x-50,y+50,z+30,1)
        space.appendatom(a)
        bond_atoms(a5,a)
        space.atoms2compute()


    if space.t==4500: #C+C
        space.compute2atoms()
        a = Atom(x-50,y+50,z+30,1)
        space.appendatom(a)
        bond_atoms(a5,a)
        space.atoms2compute()



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
