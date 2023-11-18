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



def action1(space:Space):
    (x,y,z)=(500,500,500)
    global i0,i1,i2,i3,i4,i5,i6,a1,a2,a3,n1,n2
    if space.t==1:    
        i0=space.merge_from_file("examples/simple/carbonyl.json",x,y,z)
        rot = glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
        i1=space.merge_from_file("examples/simple/OH.json",-50+x,y,+30+z, rot)
        bond_atoms(space.atoms[i0],space.atoms[i1])
        #bond_atoms(space.atoms[0],space.atoms[1])
        space.atoms2compute()

    if space.t==200:
        space.compute2atoms()
        a1 = Atom(500,500,500,4)
        space.appendatom(a1)
        bond_atoms(space.atoms[i0],a1)
        space.atoms2compute()
        pass


    if space.t==400:
        space.compute2atoms()
        h1 = Atom(500,550,500,1)
        space.appendatom(h1)
        bond_atoms(a1,h1)
        space.atoms2compute()
        pass



    if space.t==600:
        space.compute2atoms()
        ami = space.merge_from_file("examples/simple/aminogroup.json",x,y-20,z)
        #space.appendatom(a1)
        bond_atoms(a1,space.atoms[ami],3)
        space.atoms2compute()


    if space.t==800:
        space.compute2atoms()
        i2 = space.merge_from_file("examples/simple/CH2.json",x,30+y,z)
        bond_atoms(a1,space.atoms[i2])  #L/D
        space.atoms2compute()


    if space.t==1200:
        space.compute2atoms()
        i3 = space.merge_from_file("examples/simple/CH2.json",30+x,30+y,z)
        bond_atoms(space.atoms[i2],space.atoms[i3])  #L/D
        space.atoms2compute()


    if space.t==1600:
        space.compute2atoms()
        i4 = space.merge_from_file("examples/simple/CH2.json",60+x,30+y,z)
        bond_atoms(space.atoms[i4],space.atoms[i3])  #L/D
        space.atoms2compute()

    if space.t==1900:
        space.compute2atoms()
        n1 = Atom(550,520,500,3) 
        space.appendatom(n1)
        bond_atoms(n1,space.atoms[i4])
        space.atoms2compute()

    if space.t==2300:
        space.compute2atoms()
        a2 = Atom(550,540,540,4)
        space.appendatom(a2)
        bond_atoms(a2,n1)
        space.atoms2compute()


    if space.t==2600:
        space.compute2atoms()
        i6 = space.merge_from_file("examples/simple/aminogroup.json",50+x,50+y,z)
        bond_atoms(space.atoms[i6],a2)  #L/D
        space.atoms2compute()


    if space.t==2900:
        space.compute2atoms()
        h2 = Atom(520,500,500,1)
        space.appendatom(h2)
        bond_atoms(h2,n1)
        space.atoms2compute()


    if space.t==3300:
        space.compute2atoms()
        n2 = Atom(520,500,500,3)
        space.appendatom(n2)
        bond_atoms(n2,a2)
        space.atoms2compute()


    if space.t==3600:
        space.compute2atoms()
        bond_atoms(n2,a2)
        space.atoms2compute()

    if space.t==3900:
        space.compute2atoms()
        h3 = Atom(520,500,500,1)
        space.appendatom(h3)
        bond_atoms(h3,n2)
        space.atoms2compute()




if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    space.INTERACT_KOEFF = 0.6
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
