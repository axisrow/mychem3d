import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space


    for i in range(0,1000):
        #makealcohol(space,random.randint(100,900),random.randint(100,900),random.randint(100,900),3)
        space.merge_from_file("examples/simple/NH3.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        space.merge_from_file("examples/simple/H2O.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        space.merge_from_file("examples/alkene/ethylene.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))

    space.appendmixer(100)
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()

# 4.2 fps and drop
# 3.25 fps