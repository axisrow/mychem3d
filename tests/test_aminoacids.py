import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm

aminoacids = ["examples/aminoacids/alanine.json",
               "examples/aminoacids/arginine.json",
               "examples/aminoacids/asparagine.json",
               "examples/aminoacids/aspartic_acid.json",
               "examples/aminoacids/cysteine.json",
               "examples/aminoacids/glutamice_acid.json",
               "examples/aminoacids/glutamine.json",
               "examples/aminoacids/glycine.json",
               "examples/aminoacids/histidine.json",
               "examples/aminoacids/hydroxylysine.json",
               "examples/aminoacids/hydroxyproline.json",
               "examples/aminoacids/isoleucine.json",
               "examples/aminoacids/leucine.json",
               "examples/aminoacids/lysine.json",
               "examples/aminoacids/methionine.json",
               "examples/aminoacids/phenylalanine.json",
               "examples/aminoacids/proline.json",
               "examples/aminoacids/serine.json",
               "examples/aminoacids/threonine.json",
               "examples/aminoacids/tryptophan.json",
               "examples/aminoacids/tyrosine.json",
               "examples/aminoacids/valine.json"
]
#            
# #
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(1000,400,400)
    for i in range(0,100):
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)        
        i1 = space.merge_from_file(random.choice(aminoacids),x,y,z,rot)
        #space.merge_from_file("examples/alcohol/methanol.json",x,y,z)
    for i in range(0,500):
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)        
        i2 = space.merge_from_file("examples/simple/H2O.json",x,y,z,rot)
        #space.merge_from_file("examples/alcohol/methanol.json",x,y,z)

    space.update_delta = 5
     #space.recording = True
    #space.appendmixer(1)
    #space.redox.set(True)
    App.run()
#
#
#300 - 9 fps
#300 - 1delta 40 fps
#2000 - 1delta 14,34 
#2000 - 5 delta 3,89