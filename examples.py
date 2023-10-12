import random
from re import S
from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm

def makestar1(space,x,y,z):
        D=20
        space.appendatom(Atom(x,y,z,4))
        space.appendatom(Atom(x+D,y,z,2))
        space.appendatom(Atom(x+2*D,y,z,1,pi))
        space.appendatom(Atom(x-D,y,z,2))
        space.appendatom(Atom(x-2*D,y,z,1))
        space.appendatom(Atom(x,y+D,z,2,pi/2))
        space.appendatom(Atom(x,y+2*D,z,1,pi/2))
        space.appendatom(Atom(x,y-D,z,2,pi/2))
        space.appendatom(Atom(x,y-2*D,z,1,pi*3/2))


def makecyclopropane(space,x,y,z):
        space.appendatom(Atom(x,y,z,4,r=10,m=12))
        space.appendatom(Atom(x,y,z,4,r=10,m=12))
        space.appendatom(Atom(x,y,z,4,r=10,m=12))

def makeclew(space,x,y,z):
     D = 16
     f = 0
     f2 = 0
     r = 60
     for i in range (1,100):
        r = r + 1
        f += 2*pi*r/D 
        f2 = i/20
        dx = r*sin(f2)*cos(f)
        dy = r*sin(f2)*sin(f)
        dz = r*cos(f2)
        a = Atom(x+dx,y+dy,z+dx,2,r=8)
        space.appendatom(a)

        

def makemethan(space,x,y,z):
        D=17
        #f = glm.radians(109.47)-pi
        space.appendatom(Atom(x,y,z,4,r=10))
        space.appendatom(Atom(x,y,z+D,1,f=0,f2=-pi/2, r=6))
        for i in range(0,3):
            rot = glm.quat(glm.vec3(0,pi/6,i*2*pi/3))
            hx,hy,hz = rot*glm.vec3(D,0,0)
            space.appendatom(Atom(x+hx,y+hy,z+hz,1,f=i*2*pi/3+pi,f2=pi/6, r=6))

def makeethan(space,x,y,z):
        D=17
        D2=20
        #f = glm.radians(109.47)-pi
        space.appendatom(Atom(x,y,z,4,r=10))
        for i in range(0,3):
            rot = glm.quat(glm.vec3(0,pi/6,i*2*pi/3))
            hx,hy,hz = rot*glm.vec3(D,0,0)
            space.appendatom(Atom(x+hx,y+hy,z+hz,1,f=i*2*pi/3+pi,f2=pi/6, r=6))
        space.appendatom(Atom(x,y,z+D2,4,r=10,f2=pi,f=pi/6))
        for i in range(0,3):
            rot = glm.quat(glm.vec3(0,-pi/6,i*2*pi/3))
            hx,hy,hz = rot*glm.vec3(D,0,0)
            #space.appendatom(Atom(x+hx,y+hy,z+hz+D2,1,f=i*2*pi/3+pi,f2=-pi/6, r=6))


def makealkane(space,x,y,z,n):
     space.appendatom(Atom(x-3,y-15,z-5,1,f=pi/2,r=6,m=1))
     for i in range(0,n):
         f2 = i%2 * pi
         dx = -10 * (i%2) 
         dz = -5 * (i%2) 
         space.appendatom(Atom(x+dx,y+i*15,z+dz,4,f2=f2,r=10,m=12))
         if i%2 == 0:
             space.appendatom(Atom(x,y+i*15,z+17,1,f2=-pi/2,r=6,m=1))
             space.appendatom(Atom(x+17,y+i*15,z-5,1,f=pi,f2=0,r=6,m=1))
         else:
             space.appendatom(Atom(x+dx,y+i*15,z+dz-17,1,f2=pi/2,r=6,m=1))
             space.appendatom(Atom(x+dx-15,y+i*15,z+dz+5,1,f=0,f2=0,r=6,m=1))
     space.appendatom(Atom(x-5,y+n*15,z,1,f=3*pi/2,r=6,m=1))


def makealcohol(space,x,y,z,n):
     space.appendatom(Atom(x-3,y-15,z-5,1,f=pi/2,r=6,m=1))
     for i in range(0,n):
         f2 = i%2 * pi
         dx = -10 * (i%2) 
         dz = -5 * (i%2) 
         space.appendatom(Atom(x+dx,y+i*15,z+dz,4,f2=f2,r=10,m=12))
         if i%2 == 0:
             space.appendatom(Atom(x,y+i*15,z+17,2,f2=-pi/2,r=6,m=1))
             space.appendatom(Atom(x,y+i*15+5,z+20,1,f2=-pi/2,r=6,m=1))
             space.appendatom(Atom(x+17,y+i*15,z-5,1,f=pi,f2=0,r=6,m=1))
         else:
             space.appendatom(Atom(x+dx,y+i*15,z+dz-17,1,f2=pi/2,r=6,m=1))
             space.appendatom(Atom(x+dx-15,y+i*15,z+dz+5,1,f=0,f2=0,r=6,m=1))
     space.appendatom(Atom(x-5,y+n*15,z,1,f=3*pi/2,r=6,m=1))



def makemethan_old(space,x,y,z):
        D=16
        space.appendatom(Atom(x,y,z,400,r=10))
        space.appendatom(Atom(x+D,y,z,1,f=pi, r=6))
        space.appendatom(Atom(x-D,y,z,1,f=0, r=6))
        space.appendatom(Atom(x,y+D,z,1,f=3*pi/2, r=6))
        space.appendatom(Atom(x,y-D,z,1,f=pi/2, r=6))







# n - количество лучей
# m - длина лучей
def makesuperstar(space,ox,oy, oz, n,m=1):
    D=20
    f = 0
    R = D*n/pi/4*2
    for i in range(0,n):
            x = ox+cos(f)*R
            y = oy+sin(f)*R
            a1= Atom(x, y, oz, 3,2*pi/n*i)
            space.appendatom(a1)
            for j in range(0,m):
                x = ox+cos(f)*(R+D*j+D)
                y = oy+sin(f)*(R+D*j+D)
                a1= Atom(x, y, oz, 2, 2*pi/n*i)
                space.appendatom(a1)
            x = ox+cos(f)*(R+D*m+D)
            y = oy+sin(f)*(R+D*m+D)
            a1= Atom(x, y, oz,1,2*pi/n*i+pi)
            space.appendatom(a1)
            f+=2*pi/n
#
def makepoly1(space,x,y,z,n=5): 
    D=20
    a1= Atom(x-D, y, z, 1)
    space.appendatom(a1)
    a1= Atom(x+n*D, y, z, 1,pi)
    space.appendatom(a1)
    for i in range(0,n):
        a1= Atom(x+i*D, y, z,5, pi if i%2!=0 else 0)
        space.appendatom(a1)
        if i%2==0:
            a1= Atom(x+i*D, y-D,z, 2, pi/2)
            space.appendatom(a1)
            a1= Atom(x+i*D, y-2*D,z, 1, pi/2*3)
            space.appendatom(a1)
        else:
            a1= Atom(x+i*D, y+D, z, 2, pi/2*3)
            space.appendatom(a1)
            a1= Atom(x+i*D, y+2*D, z, 1, pi/2)
            space.appendatom(a1)

#
def makeformaldehyde(space,x,y,z):
    D=20
    D2 = 17
    a1= Atom(x, y, z,4,m=12)
    space.appendatom(a1)
    a1= Atom(x, y+D2,z,1,1/2*pi,r=6)
    space.appendatom(a1)
    a1= Atom(x-D2, y,z,1,0,r=6)
    space.appendatom(a1)
    a1= Atom(x+6, y-6,z, 2,pi/4+pi/2,m=16,r=8)
    space.appendatom(a1)
#
#
#
def makeH2O(space,x,y,z):
    D=14
    a1= Atom(x, y, z,2,m=16,r=8)
    space.appendatom(a1)
    a1= Atom(x+D, y, z,1,pi,r=6)
    space.appendatom(a1)
    a1= Atom(x-D, y, z, 1,0,r=6)
    space.appendatom(a1)
#
def makeCO2(space,x,y,z):
    D=20
    D2 = 16
    a1= Atom(x, y, z,4,m=12)
    space.appendatom(a1)
    a1= Atom(x+6, y-6, z,2,pi/4+pi/2,m=16,r=8)
    space.appendatom(a1)
    a1= Atom(x-6, y+6, z, 2,pi/4+pi/2,m=16,r=8)
    space.appendatom(a1)

#


def makeriboza(space,x,y,z):
    D=20
    D2 = 17
    D3 = 19
    a1= Atom(x-D2, y, z,1,2*pi)
    a1.r=6
    space.appendatom(a1)
    for i in range(0,5):
        a1= Atom(x+i*D, y,z, 4)
        a1.m=12
        space.appendatom(a1)
        if i<4:
            a1= Atom(x+i*D, y-D2,z, 1,3/2*pi)
            a1.r=6
            space.appendatom(a1)
            a1= Atom(x+i*D, y+D3,z, 2,pi/2)
            a1.r=8
            a1.m=16
            space.appendatom(a1)
            a1= Atom(x+i*D, y+D2+D3,z, 1,pi/2)
            a1.r=6
            space.appendatom(a1)
        else:
            a1= Atom(x+i*D, y+D2,z, 1,1/2*pi)
            a1.r=6
            space.appendatom(a1)
            a1= Atom(x+i*D+6, y-6,z, 2,pi/4+pi/2)
            a1.m=16
            a1.r=8
            space.appendatom(a1)

    


#            
#
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
#
    #makeCO2(space,250,50,100)
     #makeH2O(space,350,50,100)
    #makemethan_old(space, 500,500,500)
    #makeethan(space,50,100,100)
    #makestar1(space,160,100,100)
    #makesuperstar(space,500,500,500,20)
    #makesuperstar(space,700,300,100,10,5)
    #makepoly1(space,100,220,100)
    #makeriboza(space,400,400,100)
    #makeformaldehyde(space,800,100,100)
    #for i in range(0,50):
#        makemethan_old(space,random.randint(500,700),random.randint(500,700),random.randint(500,700))
#    space.appendmixer(20)
    #makeethan_old(space,500,500,500)
    #for i in range(0,50):
        #makemethan(space,random.randint(500,700),random.randint(500,700),random.randint(500,700))

#    makemethan(space, 500,500,500)
    #makeethan(space, 500,500,500)
#    makeclew(space,500,500,500)
    makealcohol(space,100,400,100,40)
    makealcohol(space,100,400,400,40)
    makealcohol(space,400,400,100,40)
    makealcohol(space,400,400,400,40)
    makealcohol(space,500,400,500,10)
    makealcohol(space,600,400,600,10)
    makealcohol(space,500,500,700,3)
    space.competitive = False
#    space.stoptime = 0
    #space.DETRACT_KOEFF1 = 0
    #space.DETRACT_KOEFF2 = 0
    #space.export = True
    #space.appendmixer(100)
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
