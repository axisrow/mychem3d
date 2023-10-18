import random
from re import S
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
    for i in range(0,100):
            #makealcohol(space,random.randint(100,900),random.randint(100,900),random.randint(100,900),3)
        space.merge_from_file("examples/simple/NH3.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
        #space.merge_from_file("examples/simple/H2O.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/alkene/etylen.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/alkane/decane.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        space.merge_from_file("examples/aldehyde/glycolaldehyde.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
    #space.export = True
    #space.merge_from_file("examples/alkane/30ane.json",glm.vec3(100,100,100))
    space.update_delta = 5  
     #space.recording = True
    space.appendmixer(1)
    space.redox = True
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
