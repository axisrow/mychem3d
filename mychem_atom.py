from math import pi,sin,cos
import glm

class Node:
	def __init__(self,parent):
		self.f = 0
		self.f2 = 0
		self.bonded = False
		self.bonded2 = False
		self.pair = None
		self.parent = parent

	def shift_q(self, n):
		#PHCSNO
		type1 = self.parent.type
		type2 = n.parent.type
		table=[5,1,4,400,6,3,2]
		i1 = table.index(type1)
		i2 = table.index(type2)
		canbond = False
		(ep1,ep2)=(None,None)
		for ep_i in self.parent.el_pairs:
			if canbond:
				break
			for ep_j in n.parent.el_pairs:
				if not ep_i.assigned and not ep_j.assigned and (ep_i.ecount+ep_j.ecount == 2):
					(ep1,ep2)=(ep_i,ep_j)
					ep1.assigned = True
					self.assigned_ep = ep1
					ep2.assigned = True
					n.assigned_ep = ep2
					canbond = True
					break
				
		if canbond:
			if i1<i2:
				(ep1.ecount, ep2.ecount) = (0,2)
			if i1>i2:
				(ep1.ecount, ep2.ecount) = (2,0)
			if i1==i2:
				(ep1.ecount, ep2.ecount) = (1,1)
		return canbond

	def bond(self,n):
		canbond = self.shift_q(n)
		if canbond:
			n.pair = self
			n.bonded = True
			self.pair = n
			self.bonded = True
		return canbond
	
	def unbond(self):
		if self.bonded:
			#
			#if self.assigned_ep.ecount == 1 and self.pair.assigned_ep.ecount == 1:
			#	if random.choice([False,True]):
			#		self.assigned_ep.ecount = 0
			#		self.pair.assigned_ep.ecount = 2
			#	else:
			#		self.assigned_ep.ecount = 2
			#		self.pair.assigned_ep.ecount = 0
			self.pair.assigned_ep.assigned = False
			self.pair.assigned_ep = None
			self.assigned_ep.assigned = False
			self.assigned_ep = None

			self.pair.pair = None
			self.pair.bonded = False
			self.pair.parent.bonded-=1
			self.pair = None
			self.bonded = False


class ElectronPairing():
	def __init__(self):
		self.ecount = 1
		self.assigned = False
		#self.node = None


class Atom:
	id = 0
	def __init__(self,x,y,z, type=1,f=0,f2=0,r=10,m=1,q=0,fixed=False):
		Atom.id += 1
		self.id = Atom.id
		self.YSHIFT = 0
		self.x = x
		self.y = y
		self.z = z
		self.pos = glm.vec3(x,y,z)
		self.vx = 0.0
		self.vy = 0.0
		self.vz = 0.0
		self.v = glm.vec3(0,0,0)
		self.ax = 0.0
		self.ay = 0.0
		self.az = 0.0
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
		if self.type==2:
			self.color = (1.0,0.0,0.0)
		if self.type==3:
			self.color = (0.5,0.5,0.5)
		if self.type==4 or self.type==400:
			self.color = (1.0, 1.0, 0.0)
		if self.type==5:
			self.color = (128/255,64/255,48/255)
		if self.type==6:
			self.color = (131/255,206/255,137/255)
		if self.type==10:
			self.color = (0.0,1.0,0.0)
		if self.type==100:
			self.color = (1.0, 0.0, 1.0)

		if self.type<6 and self.type!=4 and self.type!=2:
			for i in range(0,self.type):
				n = Node(self)
				n.f = 2*pi/self.type*i
				self.nodes.append(n)
				ep = ElectronPairing()
				self.el_pairs.append(ep)
		elif type==400: #plane carbon
			for i in range(0,4):
				n = Node(self)
				n.f = 2*pi/4*i
				self.nodes.append(n)
				ep = ElectronPairing()
				self.el_pairs.append(ep)
		elif self.type == 2:
			(n1,n2) = (Node(self),Node(self))
			n1.f = 0
			n1.f2 = 0
			n2.f= glm.radians(104.45)
			n2.f2= 0
			self.nodes.extend([n1,n2])
			(ep1,ep2) = (ElectronPairing(), ElectronPairing())
			self.el_pairs.extend([ep1,ep2])

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
			(ep1,ep2,ep3,ep4) = (ElectronPairing(), ElectronPairing(),ElectronPairing(),ElectronPairing())
			self.el_pairs.extend([ep1,ep2,ep3,ep4])
		elif self.type==6:
			(n1,n2) = (Node(self),Node(self))				
			n1.f = 0
			n2.f = pi
			self.nodes.extend([n1,n2])
			(ep1,ep2) = (ElectronPairing(), ElectronPairing())
			self.el_pairs.extend([ep1,ep2])
		elif self.type==10:
			(n1,n2,n3) = (Node(self),Node(self),Node(self))
			n1.f = 0
			n2.f = pi/2
			n3.f = pi
			self.nodes.extend([n1,n2,n3])
		self.rot = glm.quat(glm.vec3(0,-f2,f))
		self.rotv = glm.quat()



	def reset_ep(self):
		for ep in self.el_pairs:
			ep.ecount = 1
		self.calculate_q()	

	def calculate_q(self):
		q = 0
		for ep  in self.el_pairs:
			if ep.ecount==0:
				q+=1
			if ep.ecount==2:
				q-=1
		self.q = q				
		return q
			
	def unbond(self):
		for n in self.nodes:
			if n.bonded:
				p = n.pair.parent
				n.unbond()
				p.calculate_q()	
		self.calculate_q()

