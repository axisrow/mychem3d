import random
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import *



def makesomething(space,x,y,z):
        D=20
        for i in range(0,7):
                space.appendatom(Atom(x+D*i,y,z,5,pi))
                space.appendatom(Atom(x+D*i,y+D,z,4))
                space.appendatom(Atom(x+D*i,y+6*D,z,5,0))
                space.appendatom(Atom(x+D*i,y+5*D,z,4))
        for i in range(0,2):
                for j in range(0,3):
                        space.appendatom(Atom(x+D*(i+5),y+D*(j+2),z,4))
        for j in range(0,7):
               space.appendatom(Atom(x+D*7,y+D*j,z,1,pi))
        space.appendatom(Atom(x-D,y,z,1))
        space.appendatom(Atom(x-D,y+D,z,1))
        space.appendatom(Atom(x-D,y+5*D,z,1))
        space.appendatom(Atom(x-D,y+6*D,z,1))


App = mychemApp()
random.seed(1)
space = App.space
#space.stoptime = 10 
#makesomething(space,150,250,0)
#makesomething(space,350,250,0)
for i in range(0,1000):
        t = random.randint(1,4);
        a = Atom(random.randrange(1,space.WIDTH), random.randrange(1,space.HEIGHT),random.randrange(1,space.DEPTH),t )        
        for n in a.nodes:
                n.q= random.choice([-1,1])
        space.appendatom(a);
space.appendmixer(2)
#space.export = True
#space.stoptime = 0
App.run()

#import glm
#vector = glm.vec3(1,0,0);
#rotmat = glm.rotate(glm.radians(-90), (0,0,1) )
#vector = rotmat * vector
#print(vector.to_tuple())


  