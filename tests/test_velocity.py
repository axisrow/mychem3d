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


f = 0
def action1(space):
    global f
    if space.t==1:    #OH
        (x,y,z) = (500,500,500)

        i=space.merge_from_file("examples/simple/H2O.json",x,y,z)
        #space.atoms[i].v = glm.vec3(0.99,0,0)

        (x,y,z) = (530,500,500)

        a = Atom(375,610,500,1)
        a.v = glm.vec3(1.0,-1.0,0.0)
        a.nodes[0].q=1
        space.appendatom(a)


        

        space.atoms2compute()

    #if space.t>1 and space.t %4 == 0: #OH
#        space.compute2atoms()
    #    a2 = Atom(x,y,z+50,4)
    #    space.appendatom(a2)
    #    bond_atoms(space.atoms[1],a2)
#        space.atoms[46].v = glm.vec3(-0.5*sin(space.t/100),0,0)
#        space.atoms2compute()




if __name__ == '__main__':
#
    App = mychemApp()
    space = App.space
    space.setSize(1000,1000,1000)
    space.action = action1
    #space.INTERACT_KOEFF = 0.1
    space.BOND_KOEFF = 0.4
    #space.ROTA_KOEFF = 0.000001
    space.REPULSION_KOEFF1=30
    #space.REPULSION_KOEFF2=0.2
    space.update_delta = 1
    space.highlight_unbond.set(True)
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#

