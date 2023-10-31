import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm



#            
# #
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    SIZE = 400
    for i in range(0,2000):
        space.merge_from_file("examples/simple/H2O.json",random.randint(-SIZE,SIZE),random.randint(-SIZE,SIZE),random.randint(-SIZE,SIZE))
    space.update_delta = 1
     #space.recording = True
    #space.appendmixer(1)
    #space.redox.set(True)
    App.run()
#
#
#300 - 9 fps
