from math import pi as PI

class Node:
	def __init__(self,parent):
		self.f = 0
		self.bonded = False
		self.bonded2 = False
		self.pair = None
		self.canvas_id = None
		self.parent = parent

	def shift_q(self, n):
		#PHCSNO
		type1 = self.parent.type
		type2 = n.parent.type
		table=[5,1,4,6,3,2]
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
	def __init__(self,x,y,z, type=1,f=0,f2=0,r=10,m=1,q=1,fixed=False):
		Atom.id += 1
		self.id = Atom.id
		self.YSHIFT = 0
		self.x = x
		self.y = y
		self.z = z
		self.f = f
		self.f2 = f2
		self.vx = 0.0
		self.vy = 0.0
		self.ax = 0.0
		self.ay = 0.0
		self.vf = 0.0
		self.af = 0.0
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
		if self.type==4:
			self.color = (1.0, 1.0, 0.0)
		if self.type==5:
			self.color = (128/255,64/255,48/255)
		if self.type==6:
			self.color = (131/255,206/255,137/255)
		if self.type==10:
			self.color = (0.0,1.0,0.0)
		if self.type==100:
			self.color = (1.0, 0.0, 1.0)

		if self.type<6:
			for i in range(0,self.type):
				n = Node(self)
				n.f = 2*PI/self.type*i
				self.nodes.append(n)
				ep = ElectronPairing()
				self.el_pairs.append(ep)
		elif self.type==6:
			(n1,n2) = (Node(self),Node(self))				
			n1.f = 0
			n2.f = PI
			self.nodes.extend([n1,n2])
			(ep1,ep2) = (ElectronPairing(), ElectronPairing())
			self.el_pairs.extend([ep1,ep2])
		elif self.type==10:
			(n1,n2,n3) = (Node(self),Node(self),Node(self))
			n1.f = 0
			n2.f = PI/2
			n3.f = PI
			self.nodes.extend([n1,n2,n3])

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

	def draw(self,canvas):
		pass
#		self.canvas_id = canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,outline=self.color,fill=self.color)
#		for n in self.nodes:
#			nx = self.x + cos(n.f+self.f)*self.r
#			ny = self.y - sin(n.f+self.f)*self.r
#			if n.bonded:
#				n.canvas_id = canvas.create_oval(nx-1,ny-1,nx+1,ny+1,outline=self.BONDEDCOLOR,fill=self.BONDEDCOLOR)
#			else:
#				n.canvas_id = canvas.create_oval(nx-1,ny-1,nx+1,ny+1,outline=self.UNBONDEDCOLOR,fill=self.UNBONDEDCOLOR)

	def limits(self):
		if self.vx < -self.MAXVELOCITY: self.vx=-self.MAXVELOCITY
		if self.vx > self.MAXVELOCITY: self.vx=self.MAXVELOCITY
		if self.vy < -self.MAXVELOCITY: self.vy=-self.MAXVELOCITY
		if self.vy > self.MAXVELOCITY: self.vy=self.MAXVELOCITY

		if self.x < self.r: 
			self.vx= -self.vx
			self.x = self.r
		if self.x>self.space.WIDTH-self.r : 
			self.vx= -self.vx
			self.x = self.space.WIDTH-self.r
		if self.y < self.r:
			self.vy= -self.vy
			self.y = self.r
		if self.y>self.space.HEIGHT-self.r : 
			self.vy= -self.vy
			self.y= self.space.HEIGHT-self.r
		if self.f > 2*PI:
			self.f-= 2*PI
		if self.f < 0:
			self.f+= 2*PI

	def next(self):
		if not self.fixed:
#			self.vx = self.vx + self.ax
#			self.vy = self.vy + self.ay
#			self.vf = self.vf + self.af
#			self.x  = self.x+self.vx
#			self.y  = self.y+self.vy
#			self.f  = self.f+self.vf

			self.limits()
