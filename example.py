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
             space.appendatom(Atom(x,y+i*15,z+17,2,f2=-pi/2,r=6,m=16))
             space.appendatom(Atom(x,y+i*15+5,z+26,1,f2=-pi/2,r=6,m=1))
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

    
def makeplane2(space,y):
     for i in range(100,900,34):
          for j in range(200,900,60):
               a = Atom(i-17,y,j,3,m=16,r=9)
               a.rot = glm.quat(cos(pi/2.0/2.0), glm.vec3(1,0,0)* sin(pi/2.0/2.0))*glm.quat(cos(3*pi/2.0/2.0), glm.vec3(0,0,1)* sin(3*pi/2.0/2.0))
               a.calc_node_positions()
               space.appendatom(a)
               a = Atom(i,y,j+10,3,m=16,r=9)
               a.rot = glm.quat(cos(pi/2.0/2.0), glm.vec3(1,0,0)* sin(pi/2.0/2.0))*glm.quat(cos(pi/2.0/2.0), glm.vec3(0,0,1)* sin(pi/2.0/2.0))
               a.calc_node_positions()
               space.appendatom(a)
               a = Atom(i,y,j+30,3,m=16,r=9)
               a.rot = glm.quat(cos(pi/2.0/2.0), glm.vec3(1,0,0)* sin(pi/2.0/2.0))*glm.quat(cos(3*pi/2.0/2.0), glm.vec3(0,0,1)* sin(3*pi/2.0/2.0))
               a.calc_node_positions()
               space.appendatom(a)
               a = Atom(i-17,y,j+41,3,m=16,r=9)
               a.rot = glm.quat(cos(pi/2.0/2.0), glm.vec3(1,0,0)* sin(pi/2.0/2.0))*glm.quat(cos(pi/2.0/2.0), glm.vec3(0,0,1)* sin(pi/2.0/2.0))
               a.calc_node_positions()
               space.appendatom(a)



def makeplane(space,y):
     for i in range(100,900,21):
          for j in range(200,900,21):
               a = Atom(i,y,j,4,m=12,r=10)
               a.rot = glm.quat(cos(pi/2.0/2.0), glm.vec3(1,0,0)* sin(pi/2.0/2.0))
               a.calc_node_positions()
               space.appendatom(a)

def maketube(space,y,n):
     for i in range(100,900,21):
          f = 0
          l = 18*n
          r = 18*n/(2*pi)
          i = 0
          while(f<2*pi):
            dy = r* cos(f)
            dz = r* sin(f)
            a = Atom(i,y+dy,500+dz,3,m=14,r=9)
            df = 2*pi/n
            if (i%2==0):
                #a.rot = glm.quat(cos(pi/2*f), glm.vec3(1,0,0)* sin(pi/2.0*f)) * glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
                pass
            else:
                a.rot = glm.quat(cos(pi/2*f), glm.vec3(1,0,0)* sin(pi/2.0*f))
            a.calc_node_positions()
            space.appendatom(a)
            f +=df
            i+=1


def makecircle(space,y,n):
          f = 0
          l = 16*n
          r = 16*n/(2*pi)
          while(f<2*pi):
            dx = r* cos(f)
            dz = r* sin(f)
            a = Atom(500+dx,y,500+dz,200,m=16,r=8)
            df = 2*pi/n
            a.rot = glm.quat(cos(-f/2.0), glm.vec3(0,1,0)* sin(-f/2.0))*glm.quat(cos(-pi/2.0/2.0), glm.vec3(0,1,0)* sin(-pi/2.0/2.0)) 
            a.calc_node_positions()
            space.appendatom(a)
            f +=df

def makecircleplane(space,y):
     for i in range(10,180,9):
          makecircle(space,y,i)

#            
# #
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
#    makealcohol(space,500,300,500,40)
    #makealcohol(space,50,400,400,40)
    #makealcohol(space,950,400,100,40)
    #makealcohol(space,400,400,400,20)
    #makeplane(space,300)
    #makeplane(space,400)
    #makeplane(space,500)
    #makealkane(space,500,300,700,40)
    #makeplane(space,600)
    #makealcohol(space,500,400,500,10)
    #makealcohol(space,600,100,600,30)
    #makeplane(space,700)
    #makeplane2(space,200)
    #makecircleplane(space,500)

    #a = Atom(500,700,500,100,m=100,r=50)
    #a.v = glm.vec3(0,-1,0)
    #space.appendatom(a)
    #space.gpu_compute = False
    for i in range(0,100):
            #makealcohol(space,random.randint(100,900),random.randint(100,900),random.randint(100,900),3)
        space.merge_from_file("examples/simple/NH3.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        space.merge_from_file("examples/simple/H2O.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        space.merge_from_file("examples/alkene/etylen.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))

    #space.merge_from_file("examples/alkane/decane.json",0,0,0)
    #space.merge_from_file("examples/alkane/methane.json",50,50,0)
    #space.merge_from_file("examples/aldehyde/formaldehyde.json", 50,200,0)
    #makealcohol(space,500,500,700,3)
    #space.competitive = False
#    space.stoptime = 0
    #space.DETRACT_KOEFF1 = 0
    #space.DETRACT_KOEFF2 = 0
    #space.export = True
    #space.merge_from_file("examples/alkane/30ane.json",glm.vec3(100,100,100))
    space.update_delta = 10   
     #space.recording = True
    #space.appendmixer(1)
    space.redox = True
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
