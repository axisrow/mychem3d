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
    global i0,i1,index
    (x,y,z)=(500,500,500)
    if space.t==1:    # 
        i0 = space.merge_from_file("examples/alcohol/tetrabutanol.json",0,0,0)
        #rot = glm.quat(cos(pi/4), glm.vec3(0,0,sin(pi/4)))
        i1 = space.merge_from_file("examples/simple/carbonyl.json",0,+80,-20)
        space.atoms[i0+13].nodes[2].q=0
        #space.atoms[i0+5].color = (0,1,0)
        #bond_atoms(space.atoms[i0],space.atoms[i1])
        space.atoms2compute()

    if space.t==100:    # 
        space.compute2atoms()
        space.atoms[i0+17].v=glm.vec3(0,0,0)
        space.atoms[i0+17].nodes[0].q=0
        #bond_atoms(space.atoms[i0+17],space.atoms[i1])
        bond_atoms(space.atoms[i0+13],space.atoms[i1])
        
        space.atoms2compute()
        #index+=1


    if space.t==400:    #   D-riboza
        space.compute2atoms()
        space.atoms[i0+17].nodes[0].q=0
        bond_atoms(space.atoms[i0+17],space.atoms[i1])
        bond_atoms(space.atoms[i0+13],space.atoms[i1])
        space.atoms2compute()
        #index+=1


    if space.t==600:    #  
        space.compute2atoms()
        space.atoms[i0+5].nodes[0].q=0
        space.atoms[i1+1].nodes[0].q=0
        space.atoms2compute()
        #index+=1

    if space.t==2200:    #   
        space.compute2atoms()
        bond_atoms(space.atoms[i1+1], space.atoms[i0+5] )
        space.atoms2compute()

    if space.t==2300:    #   
        space.INTERACT_KOEFF=2
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.5
    #space.BONDS_KOEFF = 0.2
    space.update_delta = 5
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
