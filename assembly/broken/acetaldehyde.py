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
    global i1,i2
    (x,y,z)=(500,500,500)
    if space.t==1:    
       #space.compute2atoms()
        i1=space.merge_from_file("examples/simple/carbonyl.json",x,y,z)
        i2=space.merge_from_file("examples/simple/methyl.json",x,y,z+30)
        bond_atoms(space.atoms[i1],space.atoms[i2])
        space.atoms2compute()

    if space.t==1500: # C+H
        space.compute2atoms()
        a1 = Atom(x+10,y,z-20,1,f2=pi/2)
        space.appendatom(a1)
        bond_atoms(a1, space.atoms[i1])
        space.atoms2compute()
        

    if space.t==1500:
        #space.INTERACT_KOEFF = 0.2
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.BOND_KOEFF = 0.4
    #space.INTERACT_KOEFF = 0.1
    space.update_delta = 5
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
