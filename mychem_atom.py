from math import pi,sin,cos
from ctypes import Structure,c_float,c_bool
import glm

class NodeC(Structure):
    _fields_ = [
        ("pos", c_float*4),
        ("q", c_float),
        ("bonded", c_float),
        ("type", c_float),
        ("spin",c_float)
    ]

    def to_ctypes(self,n,space):
        self.pos[0:3] = n.pos.to_list()
        self.pos[3] = 0
        self.q = n.q 
        self.bonded = float(n.bonded)
        self.type = float(n.type)
        #self.pair = float(space.get_index_by_node(n.pair))
        self.spin = float(n.spin)
    
    def from_ctypes(self,n,space):
        #n.pos = glm.vec3(self.pos[0:3])
        n.q = self.q
        n.bonded = bool(self.bonded)
        #n.pair = space.get_node_by_index(self.pair) 
        n.spin = self.spin
        n.type = int(self.type)

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
        self.type = 0 



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
        self.q = a.q
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
        self.color[0:4]= a.color

    def from_ctypes(self,a):
        a.pos = glm.vec3(self.pos[0:3])
        a.v = glm.vec3(self.v[0:3])
        a.q = self.q
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
    def __init__(self,x,y,z, type,f=0,f2=0,fixed=False,subtype=0):
        Atom.id += 1
        self.id = Atom.id
        self.YSHIFT = 0
        self.pos = glm.vec3(x,y,z)
        self.v = glm.vec3(0,0,0)
        self.a = glm.vec3(0,0,0)
        self.type = type
        self.subtype = subtype
        self.q = 0.0
        self.nodes = []
        self.fixed = fixed
        self.near = []
        self.MAXVELOCITY = 1
        self.UNBONDEDCOLOR = (1,1,1)
        self.BONDEDCOLOR = "orange"
        
        if self.type==1:
            self.color = (0.0,0.0,1.0,1.0)
            self.r=6
            self.m=1
            n1 = Node(self)
            n1.f = 0
            n1.type = 0
            self.nodes.append(n1)
  
        if self.type==6:
            self.m=12
            self.r=10
            self.color = (1.0, 1.0, 0.0,1.0)
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

        if self.type==7:
            self.color = (0.5,0.5,0.5,1.0)
            self.m=14
            self.r=9
            for i in range(0,3):
                n = Node(self)
                n.f = 2*pi/3.0*i
                n.f2 = pi/6
                self.nodes.append(n)
            n = Node(self)    
            n.type =2 
            n.f = 0
            n.f2 = glm.radians(-90)
            self.nodes.append(n)



        if self.type==8:
            self.color = (1.0,0.0,0.0,1.0)
            self.r=8
            self.m=16
            (n1,n2,n3,n4) = (Node(self),Node(self),Node(self),Node(self))
            n1.f = 0
            n1.f2 = 0
            n2.f= glm.radians(104.45)
            n2.f2= 0
            n3.f = glm.radians(52.0)
            n3.f2 = glm.radians(120) 
            n3.type = 2
            n4.f = glm.radians(52.0)
            n4.f2 = glm.radians(-120) 
            n4.type = 2
            self.nodes.extend([n1,n2,n3,n4])


        if self.type==11: # Na
            self.color = (1.0,1.0,1.0,1.0)
            self.r=27
            self.m=23
            n1 = Node(self)
            n1.f = 0
            n1.type = 0
            self.nodes.append(n1)


        if self.type==15: #P
            self.color = (128/255,64/255,48/255,1.0)
            self.m= 31
            self.r = 12
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

        if self.type==16: #S
            self.color = (131/255,206/255,137/255,1.0)
            self.m = 32
            self.r = 12
            (n1,n2) = (Node(self),Node(self))				
            n1.f = 0
            n2.f = glm.radians(92.1)
            self.nodes.extend([n1,n2])

        if self.type==17: #Cl
            self.color = (166/255,204/255,24/255,1.0)
            self.m = 32
            self.r = 14
            n1 = Node(self)
            n1.f = 0
            n1.type = 0
            self.nodes.append(n1)



        if self.type==666:
            self.color = (1.0, 0.0, 1.0,1.0)
            self.m = 100
            self.r = 25



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


