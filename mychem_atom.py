from math import pi,sin,cos
from ctypes import Structure,c_float,c_bool
import glm

class NodeC(Structure):
    _fields_ = [
        ("pos", c_float*4),
        ("rpos", c_float*4),
        ("q", c_float),
        ("bonded", c_float),
        ("pair", c_float),
        ("spin",c_float)
    ]

    def to_ctypes(self,n,space):
        self.pos[0:3] = n.pos.to_list()
        self.pos[3] = 0
        self.q = n.q 
        self.bonded = float(n.bonded)
        print(self.bonded)
        #self.pair = float(space.get_index_by_node(n.pair))
        self.spin = float(n.spin)
    
    def from_ctypes(self,n,space):
        #n.pos = glm.vec3(self.pos[0:3])
        n.q = self.q
        n.bonded = bool(self.bonded)
        #n.pair = space.get_node_by_index(self.pair) 
        n.spin = self.spin

class Node():
    def __init__(self,parent):
        self.f = 0
        self.f2 = 0
        self.bonded = False
        self.pair = None
        self.parent = parent
        self.q = 0 
        self.spin = 0
        self.pos = glm.vec3(0,0,0)



class AtomC(Structure):
    _fields_ = [
        ("pos", c_float*4),
        ("v", c_float*4),
        ("type", c_float),
        ("r", c_float),
        ("m", c_float),
        ("ncount", c_float),
        ("rot", c_float*4),
        ("rotv", c_float*4),
        ("animate", c_float),
        ("q",  c_float),
        ("fixed", c_float),
        ("_pad1", c_float*1),
        ("color", c_float*4),
        ]
    def to_ctypes(self, a):
        self.pos[0:3]= a.pos.to_list()
        self.pos[3]= 0
        self.v[0:3]= a.v.to_list()
        self.v[3]= 0
        self.type = a.type
        self.r = a.r
        self.m = a.m
        self.ncount = len(a.nodes)
        self.fixed = float(a.fixed)
        self.rot[0]= a.rot.x
        self.rot[1]= a.rot.y
        self.rot[2]= a.rot.z
        self.rot[3]= a.rot.w
        self.rotv[0]= a.rotv.x
        self.rotv[1]= a.rotv.y
        self.rotv[2]= a.rotv.z
        self.rotv[3]= a.rotv.w
        self.animate = 0.0
        self.q = 0.0
        self.color[0:3]= a.color
        self.color[3]= 1.0

    def from_ctypes(self,a):
        a.pos = glm.vec3(self.pos[0:3])
        a.v = glm.vec3(self.v[0:3])
        a.rot.x = self.rot[0]
        a.rot.y = self.rot[1]
        a.rot.z = self.rot[2]
        a.rot.w = self.rot[3]
        a.rotv.x = self.rotv[0]
        a.rotv.y = self.rotv[1]
        a.rotv.z = self.rotv[2]
        a.rotv.w = self.rotv[3]


class Atom():
    id = 0
    def __init__(self,x,y,z, type=1,f=0,f2=0,r=10,m=1,q=0,fixed=False):
        Atom.id += 1
        self.id = Atom.id
        self.YSHIFT = 0
        self.pos = glm.vec3(x,y,z)
        self.v = glm.vec3(0,0,0)
        self.a = glm.vec3(0,0,0)
        self.vf = 0.0
        self.vf2 = 0.0
        self.m = m
        self.q = q
        self.type = type
        self.r = r
        self.nodes = []
        self.el_pairs = []
        self.bonded = 0
        self.fixed = fixed
        self.near = []
        self.MAXVELOCITY = 1
        self.UNBONDEDCOLOR = (1,1,1)
        self.BONDEDCOLOR = "orange"
        if self.type==1:
            self.color = (0.0,0.0,1.0)
            self.r=6
            self.m=1
        if self.type==2 or self.type==200:
            self.color = (1.0,0.0,0.0)
            self.r=8
            self.m=16
        if self.type==3:
            self.color = (0.5,0.5,0.5)
            self.m=14
            self.r=9
        if self.type==4 or self.type==400:
            self.m=12
            self.r=10
            self.color = (1.0, 1.0, 0.0)
        if self.type==5 or self.type==500:
            self.color = (128/255,64/255,48/255)
            self.m= 31
            self.r = 12

        if self.type==6 or self.type==600:
            self.color = (131/255,206/255,137/255)
            self.m = 32
            self.r = 12

        if self.type==10:
            self.color = (0.0,1.0,0.0)
        
        if self.type==100:
            self.color = (1.0, 0.0, 1.0)
            self.m = 100
            self.r = 25


        if self.type<6 and self.type!=4 and self.type!=2 and self.type!=5:
            for i in range(0,self.type):
                n = Node(self)
                n.f = 2*pi/self.type*i
                self.nodes.append(n)
        elif type==400: #plane carbon
            for i in range(0,4):
                n = Node(self)
                n.f = 2*pi/4*i
                self.nodes.append(n)
        elif type==500: #plane phosphor
            for i in range(0,5):
                n = Node(self)
                n.f = 2*pi/5*i
                self.nodes.append(n)


        elif type==200: # 
            (n1,n2) = (Node(self),Node(self))
            n1.f = 0
            n1.f2 = 0
            n2.f= glm.radians(180)
            n2.f2= 0
            self.nodes.extend([n1,n2])
        elif self.type == 2:
            (n1,n2) = (Node(self),Node(self))
            n1.f = 0
            n1.f2 = 0
            n2.f= glm.radians(104.45)
            n2.f2= 0
            self.nodes.extend([n1,n2])
        elif self.type==4:
            (n1,n2,n3,n4) = (Node(self),Node(self),Node(self),Node(self))
            n1.f = 0
            n1.f2 = pi/2
            n2.f= 0
            n2.f2= -glm.radians(109.47-90)
            n3.f= 2*pi/3
            n3.f2= -glm.radians(109.47-90)
            n4.f= 4*pi/3
            n4.f2= -glm.radians(109.47-90)
            self.nodes.extend([n1,n2,n3,n4])
        elif self.type==5:
            (n1,n2,n3,n4,n5) = (Node(self),Node(self),Node(self),Node(self),Node(self))
            n1.f = 0
            n1.f2 = 0
            n2.f= 2*pi/3
            n2.f2= 0
            n3.f= 4*pi/3
            n3.f2= 0
            n4.f=  0
            n4.f2= pi/2
            n5.f=  0
            n5.f2= -pi/2
            self.nodes.extend([n1,n2,n3,n4,n5])
        elif self.type==6:
            (n1,n2) = (Node(self),Node(self))				
            n1.f = 0
            n2.f = glm.radians(92.1)
            self.nodes.extend([n1,n2])
        elif self.type==600:
            (n1,n2) = (Node(self),Node(self))				
            n1.f = 0
            n2.f = pi
            self.nodes.extend([n1,n2])
        elif self.type==10:
            (n1,n2,n3) = (Node(self),Node(self),Node(self))
            n1.f = 0
            n2.f = pi/2
            n3.f = pi
            self.nodes.extend([n1,n2,n3])
        self.rot = glm.quat(glm.vec3(0,-f2,f))
        self.calc_node_positions()
        self.rotv = glm.quat()

    def calc_node_positions(self):
        for n in self.nodes:
            n.pos = glm.quat(glm.vec3(0,-n.f2,n.f)) * glm.vec3(self.r,0,0)
    
    def info(self):
        print("type=", self.type)
        bs = ""
        for n in self.nodes:
            if n.bonded: 
                bs+="1"
            else: 
                bs+="0"
        print("bonds="+bs)     


