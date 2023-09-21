import random
from re import S
from mychem3d import Space,Atom,PI
import mychem3d
from math import *


def makestar1(space,x,y,z):
        D=20
        space.appendatom(Atom(x,y,z,4))
        space.appendatom(Atom(x+D,y,z,2))
        space.appendatom(Atom(x+2*D,y,z,1,PI))
        space.appendatom(Atom(x-D,y,z,2))
        space.appendatom(Atom(x-2*D,y,z,1))
        space.appendatom(Atom(x,y+D,z,2,PI/2))
        space.appendatom(Atom(x,y+2*D,z,1,PI/2))
        space.appendatom(Atom(x,y-D,z,2,PI/2))
        space.appendatom(Atom(x,y-2*D,z,1,PI*3/2))


def makemethan(space,x,y,z):
        D=16
        space.appendatom(Atom(x,y,z,4,m=12,r=10))
        space.appendatom(Atom(x,y,z+D,1,f=0,f2=PI/2, r=6))
        f = 0 
        f2 = 2/3*PI
        dx = D* sin(f2)*cos(f)
        dy = D* sin(f2)*sin(f)
        dz = D* cos(f2)
        space.appendatom(Atom(x+dx,y+dy,z+dz,1,f=f,f2=f2-PI/2+PI, r=6))
        f = 2/3*PI
        f2 = 2/3*PI
        dx = D* sin(f2)*cos(f)
        dy = D* sin(f2)*sin(f)
        dz = D* cos(f2)
        space.appendatom(Atom(x+dx,y+dy,z+dz,1,f=2*PI-f,f2=f2-PI/2+PI, r=6))
        f= 4/3*PI
        f2 = 2/3*PI
        dx = D* sin(f2)*cos(f)
        dy = D* sin(f2)*sin(f)
        dz = D* cos(f2)
        space.appendatom(Atom(x+dx,y+dy,z+dz,1,f=PI-f,f2=f-PI/2+PI, r=6))
        
        


def makeethan(space,x,y,z):
        D=20
        D2=16
        space.appendatom(Atom(x,y,z,4,m=12))
        space.appendatom(Atom(x+D,y,z,4,m=12))
        space.appendatom(Atom(x-D2,y,z,1,r=6))
        space.appendatom(Atom(x,y-D2,z,1,PI*3/2,r=6))
        space.appendatom(Atom(x,y+D2,z,1,PI/2,r=6))
        space.appendatom(Atom(x+D+D2,y,z,1,PI,r=6))
        space.appendatom(Atom(x+D,y-D2,z,1,PI*3/2,r=6))
        space.appendatom(Atom(x+D,y+D2,z,1,PI/2,r=6))

# n - количество лучей
# m - длина лучей
def makesuperstar(space,ox,oy, oz, n,m=1):
    D=20
    f = 0
    R = D*n/PI/4*2
    for i in range(0,n):
            x = ox+cos(f)*R
            y = oy-sin(f)*R
            a1= Atom(x, y, oz, 3,2*PI/n*i)
            space.appendatom(a1)
            for j in range(0,m):
                x = ox+cos(f)*(R+D*j+D)
                y = oy-sin(f)*(R+D*j+D)
                a1= Atom(x, y, oz, 2, 2*PI/n*i)
                space.appendatom(a1)
            x = ox+cos(f)*(R+D*m+D)
            y = oy-sin(f)*(R+D*m+D)
            a1= Atom(x, y, oz,1,2*PI/n*i+PI)
            space.appendatom(a1)
            f+=2*PI/n
#
def makepoly1(space,x,y,z,n=5): 
    D=20
    a1= Atom(x-D, y, z, 1)
    space.appendatom(a1)
    a1= Atom(x+n*D, y, z, 1,PI)
    space.appendatom(a1)
    for i in range(0,n):
        a1= Atom(x+i*D, y, z,5, PI if i%2!=0 else 0)
        space.appendatom(a1)
        if i%2==0:
            a1= Atom(x+i*D, y-D,z, 2, PI/2)
            space.appendatom(a1)
            a1= Atom(x+i*D, y-2*D,z, 1, PI/2*3)
            space.appendatom(a1)
        else:
            a1= Atom(x+i*D, y+D, z, 2, PI/2*3)
            space.appendatom(a1)
            a1= Atom(x+i*D, y+2*D, z, 1, PI/2)
            space.appendatom(a1)

#
def makeformaldehyde(space,x,y,z):
    D=20
    D2 = 17
    a1= Atom(x, y, z,4,m=12)
    space.appendatom(a1)
    a1= Atom(x, y+D2,z,1,1/2*PI,r=6)
    space.appendatom(a1)
    a1= Atom(x-D2, y,z,1,0,r=6)
    space.appendatom(a1)
    a1= Atom(x+6, y-6,z, 2,PI/4+PI/2,m=16,r=8)
    space.appendatom(a1)
#
#
#
def makeH2O(space,x,y,z):
    D=14
    a1= Atom(x, y, z,2,m=16,r=8)
    space.appendatom(a1)
    a1= Atom(x+D, y, z,1,PI,r=6)
    space.appendatom(a1)
    a1= Atom(x-D, y, z, 1,0,r=6)
    space.appendatom(a1)
#
def makeCO2(space,x,y,z):
    D=20
    D2 = 16
    a1= Atom(x, y, z,4,m=12)
    space.appendatom(a1)
    a1= Atom(x+6, y-6, z,2,PI/4+PI/2,m=16,r=8)
    space.appendatom(a1)
    a1= Atom(x-6, y+6, z, 2,PI/4+PI/2,m=16,r=8)
    space.appendatom(a1)

#


def makeriboza(space,x,y,z):
    D=20
    D2 = 17
    D3 = 19
    a1= Atom(x-D2, y, z,1,2*PI)
    a1.r=6
    space.appendatom(a1)
    for i in range(0,5):
        a1= Atom(x+i*D, y,z, 4)
        a1.m=12
        space.appendatom(a1)
        if i<4:
            a1= Atom(x+i*D, y-D2,z, 1,3/2*PI)
            a1.r=6
            space.appendatom(a1)
            a1= Atom(x+i*D, y+D3,z, 2,PI/2)
            a1.r=8
            a1.m=16
            space.appendatom(a1)
            a1= Atom(x+i*D, y+D2+D3,z, 1,PI/2)
            a1.r=6
            space.appendatom(a1)
        else:
            a1= Atom(x+i*D, y+D2,z, 1,1/2*PI)
            a1.r=6
            space.appendatom(a1)
            a1= Atom(x+i*D+6, y-6,z, 2,PI/4+PI/2)
            a1.m=16
            a1.r=8
            space.appendatom(a1)

    


#            
#
#
if __name__ == '__main__':
#
    random.seed(1)
    space = Space()
#
    #makeCO2(space,250,50,100)
    #makeH2O(space,350,50,100)
    makemethan(space, 100,100,100)
    #makeethan(space,50,100,100)
    #makestar1(space,160,100,100)
    makesuperstar(space,300,200,100,20)
    makesuperstar(space,700,300,100,10,5)
    #makepoly1(space,100,220,100)
    #makeriboza(space,400,400,100)
    #makeformaldehyde(space,800,100,100)
#    space.appendmixer(5)
    space.stoptime = 3000
    #space.DETRACT_KOEFF1 = 0
    #space.DETRACT_KOEFF2 = 0
    space.export = True
    space.export_nodes = True
    #space.competitive =True
    space.go()
#
#