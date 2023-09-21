import os
import json
from math import sqrt,sin,cos,pi
import numpy as np
import random
from mychem_atom import Atom
class Space:
	def __init__(self,width=1000,height=1000,depth=100):
		self.ucounter = 0
		self.WIDTH=width
		self.HEIGHT=height
		self.DEPTH=depth
		self.ATOMRADIUS = 10
		self.BOND_KOEFF = 0.2
		self.BONDR = 4
		self.attract_k = 30
		self.ATTRACT_KOEFF= self.attract_k/100.0
		#self.ATTRACTR = 5*self.ATOMRADIUS
		self.ROTA_KOEFF = 0.00005
		self.REPULSION1 = -3
		self.repulse_k1 = 20
		self.REPULSION_KOEFF1 = self.repulse_k1
		self.REPULSION2 = 4
		self.repulse_k2 = 50
		self.REPULSION_KOEFF2= self.repulse_k2/10.0
		self.MAXVELOCITY = 1
		self.t = -1
		self.recordtime = 0
		self.atoms = []	
		self.mixers = []
		self.g = 0.01
		self.newatom = None
		self.createtype=4
		self.createf = 0
		self.standard = True
		self.merge_atoms = []
		self.merge_mixers = []
		self.select_mode = False
		self.gravity = False
		self.shake = False
		self.SHAKE_KOEFF = 3
		self.competitive = True
		self.redox = False
		self.redox_rate = 1
		self.segmented_redox = True
		self.bondlock = False
		self.linear_field = False
		self.update_delta= 5
		self.show_q = False



	def appendatom(self,a):
		a.space = self
		self.atoms.append(a)

	def appendmixer(self,n=1):
		for i in range(0,n):
			m = Atom(random.randint(1,self.WIDTH),random.randint(1,self.HEIGHT),0,100)
			m.space = self
			m.vx = 1
			m.vy = 1
			m.m = 40
			self.mixers.append(m)
			self.atoms.append(m)
	
	def atoms2numpy(self):
		N = len(self.atoms)
		self.np_r = np.empty((N))
		self.np_x = np.empty((N))
		self.np_y = np.empty((N))
		self.np_vx =np.empty((N))
		self.np_vy = np.empty((N))
		self.np_ax = np.empty((N))
		self.np_ay = np.empty((N))
		self.np_f = np.empty((N))
		self.np_vf = np.empty((N))
		self.np_type = np.empty((N))
		self.np_m = np.empty((N))
		self.np_q = np.empty((N))

		for i in range(0,N):
			atom_i = self.atoms[i]
			self.np_r[i]=atom_i.r
			self.np_m[i]=atom_i.m
			self.np_x[i]=atom_i.x
			self.np_y[i]=atom_i.y
			self.np_vx[i]=atom_i.vx
			self.np_vy[i]=atom_i.vy
			self.np_ax[i]=atom_i.ax
			self.np_ay[i]=atom_i.ay
			self.np_f[i]=atom_i.f
			self.np_vf[i]=atom_i.vf
			self.np_q[i]=atom_i.q
			self.np_type[i]=atom_i.type
		self.np_SUMRADIUS = np.add.outer(self.np_r,self.np_r)
		self.np_SUMRADIUS_D1 = self.np_SUMRADIUS + self.REPULSION1
		self.np_SUMRADIUS_D2 = self.np_SUMRADIUS + self.REPULSION2

	def numpy2atoms(self):
		N = len(self.atoms)
		for i in range(0,N):
			atom_i = self.atoms[i]
			atom_i.x=self.np_x[i]
			atom_i.y=self.np_y[i]
			atom_i.vx=self.np_vx[i]
			atom_i.vy=self.np_vy[i]
			atom_i.ax=self.np_ax[i]
			atom_i.ay=self.np_ay[i]
			atom_i.f=self.np_f[i]
			atom_i.q=self.np_q[i]

	def np_next(self):
			self.np_vx *=0.9999
			self.np_vy *=0.9999
			self.np_vf *=0.99
			self.np_vx += self.np_ax
			self.np_vy += self.np_ay
			self.np_x += self.np_vx
			self.np_y += self.np_vy
			self.np_f += self.np_vf


	def np_limits(self): 
		self.np_vx[self.np_vx< -self.MAXVELOCITY] = -self.MAXVELOCITY
		self.np_vx[self.np_vx> self.MAXVELOCITY] = self.MAXVELOCITY
		self.np_vy[self.np_vy< -self.MAXVELOCITY] = -self.MAXVELOCITY
		self.np_vy[self.np_vy> self.MAXVELOCITY] = self.MAXVELOCITY
		self.np_f[self.np_f> 2*pi] -=2*pi
		self.np_f[self.np_f< 0] += 2*pi

		b = self.np_x< self.np_r
		self.np_x[b] = self.np_r[b]
		self.np_vx[b] = - self.np_vx[b]

		b = self.np_y < self.np_r
		self.np_y[b] = self.np_r[b]
		self.np_vy[b] = - self.np_vy[b]
		
		b = self.np_x > self.WIDTH-self.np_r
		self.np_x[b] = (self.WIDTH-self.np_r)[b]
		self.np_vx[b] = - self.np_vx[b]

		b = self.np_y > self.HEIGHT-self.np_r
		self.np_y[b] = (self.HEIGHT-self.np_r)[b]
		self.np_vy[b] = - self.np_vy[b]


	def compute(self):
			self.atoms2numpy()
			N = len(self.atoms)
			self.t +=1
			#Ex=np.zeros(N)
			#Ey=np.zeros(N)
			a = np.zeros((N,N))
			#ones = np.ones((N,N)
			delta_x = np.subtract.outer(self.np_x, self.np_x)
			delta_y = np.subtract.outer(self.np_y, self.np_y)
			r2 = delta_x*delta_x + delta_y*delta_y
			r = np.sqrt(r2)
			r_reciproc = np.reciprocal(r,where=r!=0)
			a[r<self.np_SUMRADIUS_D1] = (r_reciproc*self.REPULSION_KOEFF1)[r<self.np_SUMRADIUS_D1]
			a[r<self.np_SUMRADIUS_D2] = (r_reciproc*self.REPULSION_KOEFF2)[r<self.np_SUMRADIUS_D2]
			if self.competitive:
						Q = np.outer(self.np_q, self.np_q)
						if self.linear_field:
							a+= Q*self.ATTRACT_KOEFF*0.1
						else:
							a += np.divide(Q,r,where=r!=0)*self.ATTRACT_KOEFF
			np.fill_diagonal(a,0)
			a_x = np.divide(delta_x,r,where=r!=0) *a
			a_y = np.divide(delta_y,r,where=r!=0) *a
			#a_x or a_y can contain NaN on diagonal
			np.fill_diagonal(a_x,0)
			np.fill_diagonal(a_y,0)
			Ex = a_x.sum(axis=1)
			Ey = a_y.sum(axis=1)
			for i in range(0,N):
				naf = 0
				jj = np.where(np.logical_and(r[i]>0,r[i]<40))
				#print("jj=", jj)
				allnEx = 0
				allnEy = 0
				for j in jj[0]:
					if j==i: continue
					atom_i = self.atoms[i]
					atom_j = self.atoms[j]
					for n1 in atom_i.nodes:
						#if self.redox.get():
						#	if n1
						n1x = self.np_x[i] + cos(n1.f+self.np_f[i])*atom_i.r
						n1y = self.np_y[i] - sin(n1.f+self.np_f[i])*atom_i.r

						nEx = 0
						nEy = 0
						naf = 0
						for n2 in atom_j.nodes:
							n2x = self.np_x[j] + cos(n2.f+self.np_f[j])*atom_j.r
							n2y = self.np_y[j] - sin(n2.f+self.np_f[j])*atom_j.r
							delta_x = n1x-n2x
							delta_y = n1y-n2y
							r2n = delta_x*delta_x + delta_y*delta_y
							rn = sqrt(r2n) 
							if rn==0: continue
							a = 0
							if rn<self.BONDR and not n1.bonded and not n2.bonded:
								if n1.bond(n2):
									self.np_q[i] = atom_i.calculate_q()
									self.np_q[j] = atom_j.calculate_q()
									self.np_vx[i] *=0.5
									self.np_vy[i] *=0.5
									self.np_vx[j] *=0.5
									self.np_vy[j] *=0.5
							if rn>self.BONDR and n1.pair == n2:
								if not self.bondlock:
									n1.unbond()
									self.np_q[i] = atom_i.calculate_q()
									self.np_q[j] = atom_j.calculate_q()
							if n1.pair == n2:
								if (rn>0): 
									a = -r2n*self.BOND_KOEFF
									naf += 1/rn * self.ROTA_KOEFF * (cos(n1.f+self.np_f[i])*atom_i.r * delta_y + delta_x*sin(n1.f+self.np_f[i])*atom_i.r)
									if self.redox:
										in_redox_zone = False
										redox_zone = -1 
										if self.segmented_redox and self.np_x[i]<self.WIDTH/10*1:
											redox_zone=1
											in_redox_zone = True
										if self.segmented_redox and self.np_x[i]>self.WIDTH/10*9:
											redox_zone=2
											in_redox_zone = True
										if not self.segmented_redox:
											redox_zone=0
											in_redox_zone = True
										if in_redox_zone and random.randint(0,5000)==1:
												pair_a = np
												(ep1, ep2) = (n1.assigned_ep, n2.assigned_ep)
												(ecount1,ecount2) = (n1.assigned_ep.ecount,n2.assigned_ep.ecount)
												n1.unbond()
												rc=random.choice([True,False])
												if (redox_zone==1) or (redox_zone==0 and rc):
													print("reduction")
													if ecount1 == 1:
														ecount1 = 2
													else:
														if ecount1 == 0:
															ecount1 = 1
														if ecount2 ==0:
															ecount2 = 1
												if (redox_zone==2) or (redox_zone==0 and not rc):
													print("oxidation")
													if ecount1 == 1:
														ecount1 = 0	
													else:
														if ecount2 ==2:
															ecount2 = 1
														if ecount1 == 2:
															ecount1 = 1
												(ep1.ecount,ep2.ecount) = (ecount1,ecount2)
												self.np_q[i] = atom_i.calculate_q()
												self.np_q[j] = atom_j.calculate_q()
							if not n1.bonded and not n2.bonded:
								naf += 1/rn * self.ROTA_KOEFF * (cos(n1.f+self.np_f[i])*atom_i.r * delta_y + delta_x*sin(n1.f+self.np_f[i])*atom_i.r)									
							nEx += delta_x/rn * a
							nEy += delta_y/rn * a

						allnEx = allnEx + nEx
						allnEy = allnEy + nEy
						self.np_vf[i] += naf

				Ex[i] += allnEx
				Ey[i] += allnEy
			self.np_ax= Ex/self.np_m
			self.np_ay= Ey/self.np_m

			if self.gravity:
				self.np_ay += self.g

			if self.shake:
				self.np_ax += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)
				self.np_ay += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)

			#set mixers velocity		
			if len(self.mixers)>0:
				self.np_vx[np.logical_and(self.np_type==100,self.np_vx>=0)] = 1
				self.np_vx[np.logical_and(self.np_type==100,self.np_vx<0)] = -1
				self.np_vy[np.logical_and(self.np_type==100,self.np_vy>=0)] = 1
				self.np_vy[np.logical_and(self.np_type==100,self.np_vy<0)] = -1

			#if self.action:
			#self.action(self)


			#if self.moving_mode:
			#	(cx,cy) = self.getpointer()
			#	self.newatom.x=cx + self.moving_offsetx
			#	self.newatom.y=cy + self.moving_offsety

			self.np_next()
			self.np_limits()
			self.numpy2atoms()
