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
    for i in range(0,30):
            #makealcohol(space,random.randint(100,900),random.randint(100,900),random.randint(100,900),3)
        #space.merge_from_file("examples/simple/NH3.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
        #space.merge_from_file("examples/simple/H2O.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/alkene/etylen.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/alkane/decane.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/aldehyde/formaldehyde.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
        i=space.merge_from_file("examples/nucleobase/adenosine.json",random.randint(-400,400),random.randint(-400,400),random.randint(-400,400))
        space.atoms[i+5].nodes[0].q = 1
        space.atoms[i+5].color= (0,1,0)
    #space.export = True
    #space.merge_from_file("examples/alkane/30ane.json",glm.vec3(100,100,100))
    space.update_delta = 1
    #space.recording.set(True)
    space.appendmixer(10)
    space.redox.set(True)
    
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
