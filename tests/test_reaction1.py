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
#
    for i in range(0,300):
        space.merge_from_file("examples/simple/NH3.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
        space.merge_from_file("examples/aldehyde/glycolaldehyde.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
    space.update_delta = 5
     #space.recording = True
    space.appendmixer(1)
    space.redox.set(True)
    App.run()
#
#
#300 - 9 fps  update_delta=5    nodesinter 100


