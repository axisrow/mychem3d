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



def action1(space:Space):
    if space.t==1:    #OH
        space.appendmixer(3)
        for i in range(0,500):
            x = random.randint(0,space.WIDTH)
            y = random.randint(0,space.HEIGHT)
            z = random.randint(0,space.DEPTH)
            i = space.merge_from_file("examples/simple/ch2.json",x,y,z)
            a = space.atoms[i]
            #a = Atom(x,y,z,4)
            if i%2==0:
                a.nodes[2].q=+1
                a.nodes[3].q=-1
            else:
                a.nodes[2].q=+1
                a.nodes[3].q=-1

            

        
        space.atoms2compute()

    #if space.t==450: #OH
    #    space.compute2atoms()
    #    a2 = Atom(x,y,z+50,4)
    #    space.appendatom(a2)
    #    bond_atoms(space.atoms[1],a2)
    #    space.atoms2compute()




if __name__ == '__main__':
#
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.
    #space.BOND_KOEFF = 0.2
#    space.ROTA_KOEFF = 2
    #space.REPULSION_KOEFF2=0
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
