import random
from mychem3d import Space,Atom,PI
from math import *


random.seed(1)
space = Space()

def makesomething(x,y,z):
        D=20
        for i in range(0,7):
                space.appendatom(Atom(x+D*i,y,z,5,PI))
                space.appendatom(Atom(x+D*i,y+D,z,4))
                space.appendatom(Atom(x+D*i,y+6*D,z,5,0))
                space.appendatom(Atom(x+D*i,y+5*D,z,4))
        for i in range(0,2):
                for j in range(0,3):
                        space.appendatom(Atom(x+D*(i+5),y+D*(j+2),z,4))
        for j in range(0,7):
               space.appendatom(Atom(x+D*7,y+D*j,z,1,PI))
        space.appendatom(Atom(x-D,y,z,1))
        space.appendatom(Atom(x-D,y+D,z,1))
        space.appendatom(Atom(x-D,y+5*D,z,1))
        space.appendatom(Atom(x-D,y+6*D,z,1))

#space.stoptime = 10
makesomething(150,250,0)
makesomething(350,250,0)
for i in range(0,50):
        space.appendatom(Atom(random.randrange(1,space.WIDTH), random.randrange(1,space.HEIGHT),random.randrange(1,space.HEIGHT), 1));
#space.appendmixer(20)
space.export = True
#space.stoptime = 2
space.go()

