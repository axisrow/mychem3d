# -*- coding: utf-8 -*-
from time import sleep
from tkinter import *
from math import *
import random
import os
import json
from json import encoder
#encoder.FLOAT_REPR = lambda o: format(o, '.3f')

PI = 3.1415926535
from PIL import ImageGrab


class Node:
	def __init__(self):
		self.f = 0
		self.f2 = PI/2
		self.bonded = False
		self.pair = None
		self.canvas_id = None
		pass
	def bond(self,n):
		n.pair = self
		n.bonded = True
		self.pair = n
		self.bonded = True

	def unbond(self):
		if self.bonded:
			self.pair.pair = None
			self.pair.bonded = False
			self.pair = None
			self.bonded = False

class Atom:
	id = 0
	def __init__(self,x,y,z,type=1,f=0,f2=0,r=10,m=1,fixed=False):
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
		self.vz = 0.0
		self.ax = 0.0
		self.ay = 0.0
		self.az = 0.0
		self.vf = 0.0
		self.af = 0.0
		self.vf2 = 0.0
		self.af2 = 0.0
		self.m = m
		self.q = 1
		self.type = type
		self.r = r
		self.nodes = []
		self.fixed = fixed
		self.near = []
		self.MAXVELOCITY = 1
		self.UNBONDEDCOLOR = "white"
		self.BONDEDCOLOR = "orange"
		
		if self.type==1:
			self.color = "blue"
		if self.type==2:
			self.color = "red"
		if self.type==3:
			self.color = "grey"
		if self.type==4:
			self.color = "yellow"
		if self.type==5:
			self.color = "brown"
		if self.type==10:
			self.color = "magenta"

		if self.type<4:
			for i in range(0,self.type):
				n = Node()
				n.f = 2*PI/self.type*i
				self.nodes.append(n)
		elif self.type==4:
			(n1,n2,n3,n4) = (Node(),Node(),Node(),Node())
			n1.f = 0
			n2.f = PI/3*2
			n3.f = PI/3*4
			n4.f = 0
			n1.f2 = 2.0/3*PI
			n2.f2 = 2.0/3*PI
			n3.f2 = 2.0/3*PI
			n4.f2 = 0
			self.nodes.extend([n1,n2,n3,n4])

		elif self.type==5:
			(n1,n2,n3) = (Node(),Node(),Node())
			n1.f = 0
			n2.f = PI/2
			n3.f = PI
			self.nodes.extend([n1,n2,n3])

	def limits(self):
		if self.vx < -self.MAXVELOCITY: self.vx=-self.MAXVELOCITY
		if self.vx > self.MAXVELOCITY: self.vx=self.MAXVELOCITY
		if self.vy < -self.MAXVELOCITY: self.vy=-self.MAXVELOCITY
		if self.vy > self.MAXVELOCITY: self.vy=self.MAXVELOCITY
		if self.vz < -self.MAXVELOCITY: self.vz=-self.MAXVELOCITY
		if self.vz > self.MAXVELOCITY: self.vz=self.MAXVELOCITY


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
		if self.z < self.r:
			self.vz= -self.vz
			self.z = self.r
		if self.z>self.space.DEPTH-self.r : 
			self.vz= -self.vz
			self.z= self.space.DEPTH-self.r

		if self.f > 2*PI:
			self.f-= 2*PI
		if self.f < 0:
			self.f+= 2*PI

	def next(self):
		if not self.fixed:
			self.vx = self.vx + self.ax
			self.vy = self.vy + self.ay
			self.vz = self.vz + self.az
			self.vf = self.vf + self.af
			self.x  = self.x + self.vx
			self.y  = self.y + self.vy
			self.z  = self.z + self.vz
			self.f  = self.f + self.vf
			self.f2  = self.f2 + self.vf2
			self.limits()

		

class Space:
	def __init__(self,width=1024,height=576,depth=1024):
		self.WIDTH=width
		self.HEIGHT=height
		self.DEPTH=depth
		self.ATOMRADIUS = 10
		self.BOND_KOEFF = 0.2
		self.BONDR = 4
		self.ATTRACT_KOEFF= 0.05
		self.ATTRACTR = 5*self.ATOMRADIUS
		self.ROTA_KOEFF = 0.00005
		self.REPULS1 = -3
		self.REPULS_KOEFF1 = 15
		self.REPULS2 = 5
		self.REPULS_KOEFF2= 5
		self.competitive = False
		self.t = -1
		self.atoms = []	
		self.mixers = []
		self.action = None
		self.activemixer = False
		self.recording = False
		self.export = False
		self.export_nodes = False
		self.export_file = "mychem.json"
		self.exportf = None
		
		self.stoptime = -1
		self.counter_bonded = 0
		self.g = 0.01
		self.gravity = False
		if not os.path.exists('output'):
			os.makedirs('output')

	def appendatom(self,a):
		a.space = self
		self.atoms.append(a)
		#a.draw(self)

	def do_export(self):
		frame = {}
		frame["t"] = self.t
		frame["as"] = []
		N = len(self.atoms)
		for i in range(0,N):
			atom = {}
			atom["id"] = self.atoms[i].id
			atom["tp"] = self.atoms[i].type
			atom["x"] = round(self.atoms[i].x,4)
			atom["y"] = round(self.atoms[i].y,4)
			atom["z"] = round(self.atoms[i].z,4)
			atom["f"] = round(self.atoms[i].f,4)
			atom["f2"] = round(self.atoms[i].f2,4)
			atom["r"] = self.atoms[i].r
			if self.export_nodes:
				atom["ns"]=[]
				for n in self.atoms[i].nodes:
					actual_f  = n.f  + self.atoms[i].f
					actual_f2 = n.f2 + self.atoms[i].f2
					node = {}
					node["x"] = self.atoms[i].x + self.atoms[i].r * sin(actual_f2)*cos(actual_f)	
					node["y"] = self.atoms[i].y - self.atoms[i].r * sin(actual_f2)*sin(actual_f)
					node["z"] = self.atoms[i].z + self.atoms[i].r * cos(actual_f2)
					atom["ns"].append(node)
			frame["as"].append(atom)
		if not(self.exportf):
			self.exportf = open("output/" + self.export_file, "w")
		self.exportf.write(json.dumps(frame)+"\n")

		#			j = 
	def go(self):	
		K = 1
		while(1):
			N = len(self.atoms)
			self.t +=1
			for i in range(0,N):
				Ex=0
				Ey=0
				Ez=0
				a = 0
				if self.t%30==0:
					for j in range(0,N):
						a=0	
						if i==j: continue
			
						delta_x = self.atoms[i].x-self.atoms[j].x
						delta_y = self.atoms[i].y-self.atoms[j].y
						delta_z = self.atoms[i].z-self.atoms[j].z
						r2 = delta_x*delta_x+ delta_y*delta_y + delta_z*delta_z
						r = sqrt(r2)
						if r<self.ATOMRADIUS*8 and not j in self.atoms[i].near:
							self.atoms[i].near.append(j)
						if r>=self.ATOMRADIUS*8: 
							try:
								self.atoms[i].near.remove(j)
							except:
								pass

				for j in self.atoms[i].near:
					a=0	
					if i==j: continue

					delta_x = self.atoms[i].x-self.atoms[j].x
					delta_y = self.atoms[i].y-self.atoms[j].y
					delta_z = self.atoms[i].z-self.atoms[j].z
					r2 = delta_x*delta_x+ delta_y*delta_y + delta_z*delta_z
					r = sqrt(r2)
					SUMRADIUS = self.atoms[i].r+self.atoms[j].r
					AVGRADIUS = SUMRADIUS/2
					#if r>self.ATOMRADIUS*5:continue
					if r2 == 0:
						continue;

					# a> 0 отталкивание
					if r<SUMRADIUS+self.REPULS1:
						a = 1/r*self.REPULS_KOEFF1

					if r<SUMRADIUS+self.REPULS2:
						a = 1/r*self.REPULS_KOEFF2

					Ex = Ex + delta_x/r *a
					Ey = Ey + delta_y/r *a
					Ez = Ez + delta_z/r *a
					#if Ex>0.1: Ex=0.1
					#if Ex<-0.1: Ex=-0.1
					#if Ey>0.1: Ey=0.1
					#if Ey<-0.1: Ey=-0.1
					allnEx = 0
					allnEy = 0
					allnEz = 0
				
					
					for n1 in self.atoms[i].nodes:
						actual_f  = n1.f  + self.atoms[i].f
						actual_f2 = n1.f2 + self.atoms[i].f2
						#n1x = self.atoms[i].x + self.atoms[i].r * sin(actual_f2)*cos(actual_f)
						#n1y = self.atoms[i].y - self.atoms[i].r * sin(actual_f2)*sin(actual_f)
						#n1z = self.atoms[i].z + self.atoms[i].r * cos(actual_f2)
						nEx = 0
						nEy = 0
						nEz = 0
						naf = 0
						naf2 = 0
						for n2 in self.atoms[j].nodes:
							actual_f  = n2.f  + self.atoms[j].f
							actual_f2 = n2.f2 + self.atoms[j].f2
							n2x = self.atoms[j].x + self.atoms[j].r * sin(actual_f2)*cos(actual_f)
							n2y = self.atoms[j].y - self.atoms[j].r * sin(actual_f2)*sin(actual_f)
							n2z = self.atoms[j].z + self.atoms[j].r * cos(actual_f2)
							delta_x = self.atoms[i].x-n2x
							delta_y = self.atoms[i].y-n2y
							delta_z = self.atoms[i].z-n2z
							delta_f = 
							#delta_f = (n1.f-self.atoms[i].f) - (n2.f-self.atoms[j].f) 
							r2 = delta_x*delta_x + delta_y*delta_y + delta_z*delta_z
							rn = sqrt(r2) 
							#if rn==0: continue
							a = 0
							if rn<self.BONDR and not n1.bonded and not n2.bonded:
								n1.bond(n2)
								self.counter_bonded+=1
								#print('bond '+str(i)+' '+str(j))
							if rn>self.BONDR and n1.pair == n2:
								n1.unbond()
								self.counter_bonded-=1
								#print('unbond '+str(i)+' '+str(j))
							if n1.pair == n2:
								if (rn>0): 
									a = -r2*self.BOND_KOEFF
									actual_f = n1.f+self.atoms[i].f
									actual_f2 = n1.f2+self.atoms[i].f2
									naf += 1/rn * self.ROTA_KOEFF * sin(actual_f2)*(cos(actual_f)*self.atoms[i].r * delta_y + delta_x*sin(actual_f2)*sin(actual_f)*self.atoms[i].r)
									naf2 += 1/rn * self.ROTA_KOEFF * (cos(actual_f2)*self.atoms[i].r * delta_z )
							#if not n1.bonded and not n2.bonded and rn<self.ATTRACTR and r>self.ATOMRADIUS	:
							elif self.competitive:
								#a = -0.0005
								a = -1/rn*self.ATTRACT_KOEFF
								naf += 1/rn * self.ROTA_KOEFF * (cos(n1.f+self.atoms[i].f)*self.atoms[i].r * delta_y + delta_x*sin(n1.f+self.atoms[i].f)*self.atoms[i].r)
								#naf2 += 1/rn * self.ROTA_KOEFF * (cos(n1.f2+self.atoms[i].f2)*self.atoms[i].r * delta_z)

							nEx = nEx + delta_x/rn * a
							nEy = nEy + delta_y/rn * a
							nEz = nEz + delta_z/rn * a

						allnEx = allnEx + nEx
						allnEy = allnEy + nEy
						allnEz = allnEz + nEz
						self.atoms[i].vf = self.atoms[i].vf + naf
						self.atoms[i].vf2 = self.atoms[i].vf2 + naf2

					Ex+= allnEx
					Ey+= allnEy
					Ez+= allnEz



				self.atoms[i].ax= K*self.atoms[i].q*Ex/self.atoms[i].m 
				self.atoms[i].ay= K*self.atoms[i].q*Ey/self.atoms[i].m				
				self.atoms[i].az= K*self.atoms[i].q*Ez/self.atoms[i].m				
				if self.gravity:
					self.atoms[i].az +=self.g

			if self.action:
				self.action(self)
	
			for i in range(0,N):
				self.atoms[i].vx *= 0.9999
				self.atoms[i].vy *= 0.9999
				self.atoms[i].vz *= 0.9999
				self.atoms[i].vf *= 0.99
				self.atoms[i].vf2 *= 0.99
				self.atoms[i].next()
			
			#  canvas.after(1)
			#	if(time%1 ==0):  
			#		for i in range(0,N):	

			if self.stoptime!= -1:
				if self.t<self.stoptime:
					self.do_export()
				else:
					break
			else:				
				self.do_export()

			
			if self.t%100 ==0:
				print(f't={self.t} bonded={self.counter_bonded} ' )
			#time.sleep(0.005)
  

			


