import random
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom
from math import *




App = mychemApp()
random.seed(1)
space = App.space
space.tranparentmode = True
#space.stoptime = 10 
#makesomething(space,150,250,0)
#makesomething(space,350,250,0)
#for i in range(0,200):
#        space.appendatom(Atom(random.randrange(1,space.WIDTH/5), random.randrange(1,space.HEIGHT/5),random.randrange(1,space.DEPTH/5), 1, m=1,r=6));
        #space.appendatom(Atom(random.randrange(1,space.WIDTH/5), random.randrange(1,space.HEIGHT/5),random.randrange(1,space.DEPTH/5), 2, m=16,r=8)    );
        #space.appendatom(Atom(random.randrange(1,space.WIDTH/5), random.randrange(1,space.HEIGHT/5),random.randrange(1,space.DEPTH/5), 4, m=12,r=10));
        #space.appendatom(Atom(random.randrange(1,100), random.randrange(1,100),random.randrange(1,100), random.randrange(1,6)));
a = Atom(450,500,500,8,f=0, f2=0)
a.color = (a.color[0],a.color[1],a.color[2],0.1)
a.r = 200
#a.nodes[0].q = -1

space.debug = True
space.appendatom(a)        

#space.appendatom(a3)      

#space.appendmixer(2)
#space.export = True
#space.stoptime = 0
App.run()

#import glm
#vector = glm.vec3(1,0,0);
#rotmat = glm.rotate(glm.radians(-90), (0,0,1) )
#vector = rotmat * vector
#print(vector.to_tuple())


  