import os
import json
from math import sqrt,sin,cos,pi,acos
import numpy as np
import random
from mychem_atom import Atom
import glm
class Space:
    def __init__(self,width=1000,height=1000,depth=1000):
        self.ucounter = 0
        self.debug = False
        self.WIDTH=width
        self.HEIGHT=height
        self.DEPTH=depth
        self.ATOMRADIUS = 10
        self.BOND_KOEFF = 0.2
        self.BONDR = 4
        self.attract_k = 50
        self.ATTRACT_KOEFF= self.attract_k/100.0
        #self.ATTRACTR = 5*self.ATOMRADIUS
        self.ROTA_KOEFF = 0.0005
        self.REPULSION1 = -3
        self.repulse_k1 = 15
        self.REPULSION_KOEFF1 = self.repulse_k1
        self.REPULSION2 = 6
        self.repulse_k2 = 15
        self.REPULSION_KOEFF2= self.repulse_k2/10.0
        self.MAXVELOCITY = 1
        self.t = -1
        self.stoptime = -1
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
        self.merge_pos = glm.vec3(0,0,0)
        self.merge_rot = glm.quat()
        self.merge_center = glm.vec3(0,0,0)
        self.select_mode = False
        self.select_i = 0 
        self.gravity = False
        self.shake = False
        self.SHAKE_KOEFF = 0.5
        self.competitive = True
        self.redox = False
        self.redox_rate = 1
        self.segmented_redox = True
        self.bondlock = False
        self.linear_field = False
        self.update_delta= 5
        self.show_q = False
        self.action = None


    def appendatom(self,a):
        a.space = self
        self.atoms.append(a)

    def appendmixer(self,n=1):
        for i in range(0,n):
            m = Atom(random.randint(1,self.WIDTH),random.randint(1,self.HEIGHT),random.randint(1,self.DEPTH),100)
            m.space = self
            m.vx = 1
            m.vy = 1
            m.vz = 1
            m.m = 40
            self.mixers.append(m)
            self.atoms.append(m)
    
    def atoms2numpy(self):
        N = len(self.atoms)
        self.np_r = np.empty((N))
        self.np_x = np.empty((N))
        self.np_y = np.empty((N))
        self.np_z = np.empty((N))
        self.np_vx =np.empty((N))
        self.np_vy = np.empty((N))
        self.np_vz = np.empty((N))
        self.np_ax = np.empty((N))
        self.np_ay = np.empty((N))
        self.np_az = np.empty((N))
        self.np_type = np.empty((N))
        self.np_m = np.empty((N))
        self.np_q = np.empty((N))
        self.np_rot = glm.array.zeros(N,glm.quat)
        self.np_rotv = glm.array.zeros(N,glm.quat)


        for i in range(0,N):
            atom_i = self.atoms[i]
            self.np_r[i]=atom_i.r
            self.np_m[i]=atom_i.m
            self.np_x[i]=atom_i.x
            self.np_y[i]=atom_i.y
            self.np_z[i]=atom_i.z
            self.np_vx[i]=atom_i.vx
            self.np_vy[i]=atom_i.vy
            self.np_vz[i]=atom_i.vz
            self.np_ax[i]=atom_i.ax
            self.np_ay[i]=atom_i.ay
            self.np_az[i]=atom_i.az
            self.np_rot[i]=atom_i.rot
            self.np_rotv[i]=atom_i.rotv
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
            atom_i.z=self.np_z[i]
            atom_i.vx=self.np_vx[i]
            atom_i.vy=self.np_vy[i]
            atom_i.vz=self.np_vz[i]
            atom_i.ax=self.np_ax[i]
            atom_i.ay=self.np_ay[i]
            atom_i.az=self.np_az[i]
            atom_i.q=self.np_q[i]
            atom_i.rot = self.np_rot[i]
            atom_i.rotv = self.np_rotv[i]

    def np_next(self):
            self.np_vx *=0.9999
            self.np_vy *=0.9999
            self.np_vz *=0.9999
            self.np_vx += self.np_ax
            self.np_vy += self.np_ay
            self.np_vz += self.np_az
            self.np_x += self.np_vx
            self.np_y += self.np_vy
            self.np_z += self.np_vz
            self.np_rot = self.np_rotv*self.np_rot


    def np_limits(self): 
        self.np_vx[self.np_vx< -self.MAXVELOCITY] = -self.MAXVELOCITY
        self.np_vx[self.np_vx> self.MAXVELOCITY] = self.MAXVELOCITY
        self.np_vy[self.np_vy< -self.MAXVELOCITY] = -self.MAXVELOCITY
        self.np_vy[self.np_vy> self.MAXVELOCITY] = self.MAXVELOCITY
        self.np_vz[self.np_vz< -self.MAXVELOCITY] = -self.MAXVELOCITY
        self.np_vz[self.np_vz> self.MAXVELOCITY] = self.MAXVELOCITY

        b = self.np_x< self.np_r
        self.np_x[b] = self.np_r[b]
        self.np_vx[b] = - self.np_vx[b]

        b = self.np_y < self.np_r
        self.np_y[b] = self.np_r[b]
        self.np_vy[b] = - self.np_vy[b]

        b = self.np_z < self.np_r
        self.np_z[b] = self.np_r[b]
        self.np_vz[b] = - self.np_vz[b]


        b = self.np_x > self.WIDTH-self.np_r
        self.np_x[b] = (self.WIDTH-self.np_r)[b]
        self.np_vx[b] = - self.np_vx[b]

        b = self.np_y > self.HEIGHT-self.np_r
        self.np_y[b] = (self.HEIGHT-self.np_r)[b]
        self.np_vy[b] = - self.np_vy[b]

        b = self.np_z > self.DEPTH-self.np_r
        self.np_z[b] = (self.DEPTH-self.np_r)[b]
        self.np_vz[b] = - self.np_vz[b]


    def get_mergeobject_center(self):
         sum = glm.vec3(0,0,0)
         N = len(self.merge_atoms)
         for a in self.merge_atoms:
              sum += a.pos
         center = sum/N
         print("center=",center)
         return center
    
            
              

    def compute(self):
            N = len(self.atoms)
#            if N==0:
#                return 0
            self.t +=1
            if self.stoptime!= -1:
                if self.t>self.stoptime:
                    return 0


            #Ex=np.zeros(N)
            #Ey=np.zeros(N)
            a = np.zeros((N,N))
            #ones = np.ones((N,N)
            delta_x = np.subtract.outer(self.np_x, self.np_x)
            delta_y = np.subtract.outer(self.np_y, self.np_y)
            delta_z = np.subtract.outer(self.np_z, self.np_z)
            r2 = delta_x*delta_x + delta_y*delta_y + delta_z*delta_z
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
                        if self.debug: 
                            print(f"a={a} \nq={Q}")
            np.fill_diagonal(a,0)
            a_x = np.divide(delta_x,r,where=r!=0) *a
            a_y = np.divide(delta_y,r,where=r!=0) *a
            a_z = np.divide(delta_z,r,where=r!=0) *a
            #a_x or a_y can contain NaN on diagonal
            np.fill_diagonal(a_x,0)
            np.fill_diagonal(a_y,0)
            np.fill_diagonal(a_z,0)
            Ex = a_x.sum(axis=1)
            Ey = a_y.sum(axis=1)
            Ez = a_z.sum(axis=1)
            for i in range(0,N):
                totalrotv = glm.quat()
                jj = np.where(np.logical_and(r[i]>0,r[i]<60))
                #print("jj=", jj)
                allnEx = 0
                allnEy = 0
                allnEz = 0
                for j in jj[0]:
                    if j==i: continue
                    atom_i = self.atoms[i]
                    atom_j = self.atoms[j]
                    for n1 in atom_i.nodes:
                        r1 = glm.quat(glm.vec3(0,-n1.f2,n1.f)) * glm.vec3(atom_i.r,0,0)
                        v1 =  self.np_rot[i] * r1
                        (n1x, n1y, n1z) = v1
                        nEx = 0
                        nEy = 0
                        nEz = 0
                        for n2 in atom_j.nodes:
                            r2 = glm.quat(glm.vec3(0,-n2.f2,n2.f)) * glm.vec3(atom_j.r,0,0)
                            v3= (n2x, n2y, n2z)  = self.np_rot[int(j)] * r2

                            delta_x = n1x-n2x + self.np_x[i] - self.np_x[j]
                            delta_y = n1y-n2y + self.np_y[i] - self.np_y[j]
                            delta_z = n1z-n2z + self.np_z[i] - self.np_z[j]
                            #v2 = glm.vec3(delta_x, delta_y, delta_z)
                            v2 = glm.vec3(n2x + self.np_x[j] - self.np_x[i],
                                          n2y + self.np_y[j] - self.np_y[i],
                                          n2z + self.np_z[j] - self.np_z[i])
                            
                            r2n = delta_x*delta_x + delta_y*delta_y + delta_z*delta_z
                            rn = sqrt(r2n) 
                            if rn==0: continue
                            a = 0
                            if rn<self.BONDR and not n1.bonded and not n2.bonded:
                                if n1.bond(n2):
                                    if self.debug:
                                        print("bond")
                                    self.np_q[i] = atom_i.calculate_q()
                                    self.np_q[j] = atom_j.calculate_q()
                                    self.np_vx[i] *=0.5
                                    self.np_vy[i] *=0.5
                                    self.np_vz[i] *=0.5
                                    self.np_vx[j] *=0.5
                                    self.np_vy[j] *=0.5
                                    self.np_vz[j] *=0.5
                            if rn>self.BONDR and n1.pair == n2:
                                if not self.bondlock:
                                    n1.unbond()
                                    self.np_q[i] = atom_i.calculate_q()
                                    self.np_q[j] = atom_j.calculate_q()
                            if n1.pair == n2:
                                    a = -r2n*self.BOND_KOEFF  #atom's bond force
#                            if (not n1.bonded and not n2.bonded):
#                                a = -0.001
                            if (n1.pair == n2) or (not n1.bonded and not n2.bonded):
                                    if self.debug: print(f"v1={v1}, v2={v2}, v3={v3}")
                                    v1 = glm.normalize(v1)
                                    v2 = glm.normalize(v2)
                                    if self.debug: print(f"v1n={v1}, v2n={v2}")
                                    dt = glm.dot(v1,v2)
                                    if dt>1: dt=1
                                    if dt<-1: dt=-1
                                    #print(dt)
                                    if v1!=v2:
                                        axis = glm.normalize(glm.cross(v1,v2))
                                        angle = acos(dt)
                                        angle_a=angle*self.ROTA_KOEFF/100
                                        rot = glm.quat(cos(angle_a/2), sin(angle_a/2)*glm.vec3(axis))
                                        totalrotv = rot * totalrotv
                                    #naf2=0
                                        if self.debug: print(f"axis={axis} angle={angle} dt={dt}")
                            nEx += delta_x/rn * a
                            nEy += delta_y/rn * a
                            nEz += delta_z/rn * a

                        allnEx = allnEx + nEx
                        allnEy = allnEy + nEy
                        allnEz = allnEz + nEz
                        
                self.np_rotv[i] = totalrotv * self.np_rotv[i]
                
                Ex[i] += allnEx
                Ey[i] += allnEy
                Ez[i] += allnEz
                if self.debug: print("##")
            self.np_ax= Ex/self.np_m
            self.np_ay= Ey/self.np_m
            self.np_az= Ez/self.np_m
            #print(self.np_az)


            if self.gravity:
                self.np_ay -= self.g

            if self.shake:
                self.np_ax += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)
                self.np_ay += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)
                self.np_az += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)

            #set mixers velocity		
            if len(self.mixers)>0:
                self.np_vx[np.logical_and(self.np_type==100,self.np_vx>=0)] = 1
                self.np_vx[np.logical_and(self.np_type==100,self.np_vx<0)] = -1
                self.np_vy[np.logical_and(self.np_type==100,self.np_vy>=0)] = 1
                self.np_vy[np.logical_and(self.np_type==100,self.np_vy<0)] = -1
                self.np_vz[np.logical_and(self.np_type==100,self.np_vz>=0)] = 1
                self.np_vz[np.logical_and(self.np_type==100,self.np_vz<0)] = -1




            #if self.moving_mode:
            #	(cx,cy) = self.getpointer()
            #	self.newatom.x=cx + self.moving_offsetx
            #	self.newatom.y=cy + self.moving_offsety

            self.np_next()
            self.np_limits()
            
            
            if self.action:
                self.action(self)            
            #self.numpy2atoms()
            return N


    def make_export(self):
        frame = {}
        frame["vers"] = "1.0"
        frame["time"] = self.t
        frame["atoms"] = []
        N = len(self.atoms)
        for i in range(0,N):
            atom = {}
            atom["id"] = self.atoms[i].id
            atom["type"] = self.atoms[i].type
            atom["x"] = round(self.atoms[i].pos.x,4)
            atom["y"] = round(self.atoms[i].pos.y,4)
            atom["z"] = round(self.atoms[i].pos.z,4)
            #atom["f"] = round(self.atoms[i].f,4)
            #atom["f2"] = round(self.atoms[i].f2,4)
            atom["rot"] = self.atoms[i].rot.to_tuple()
            atom["vx"] = round(self.atoms[i].v.x,4)
            atom["vy"] = round(self.atoms[i].v.y,4)
            atom["vz"] = round(self.atoms[i].v.z,4)
            atom["q"] = self.atoms[i].q
            atom["m"] = self.atoms[i].m
            atom["r"] = self.atoms[i].r
            frame["atoms"].append(atom)
        return frame

    def load_data(self, j, merge=False):
        if not merge: 
            self.atoms = []
            self.mixers = []
        for a in j["atoms"]:
            type = a["type"]
            if "z" in a:
                z = a["z"]
                vz = a["vz"]
                rot = glm.quat(a["rot"])
            else:
                z = 500
                vz = 0
                if type==4: type=400
                rot = glm.quat(glm.vec3(0,0,-a["f"]))
            aa = Atom(a["x"],a["y"],z, type=type)
            aa.v = glm.vec3(a["vx"],a["vy"],vz)
            aa.rot = rot
            aa.q=a["q"]
            aa.m=a["m"]
            aa.r=a["r"]
#            if not "version" in j:
#                 aa.f= 2*pi - aa.f
            if merge:
                aa.space = self
                self.merge_atoms.append(aa)
                if type == 100:
                    self.merge_mixers.append(aa)
            else:
                self.appendatom(aa)
                if type == 100:
                    self.mixers.append(aa)
        			



##redox
                                    # if self.redox:
                                    # 	in_redox_zone = False
                                    # 	redox_zone = -1 
                                    # 	if self.segmented_redox and self.np_x[i]<self.WIDTH/10*1:
                                    # 		redox_zone=1
                                    # 		in_redox_zone = True
                                    # 	if self.segmented_redox and self.np_x[i]>self.WIDTH/10*9:
                                    # 		redox_zone=2
                                    # 		in_redox_zone = True
                                    # 	if not self.segmented_redox:
                                    # 		redox_zone=0
                                    # 		in_redox_zone = True
                                    # 	if in_redox_zone and random.randint(0,5000)==1:
                                    # 			pair_a = np
                                    # 			(ep1, ep2) = (n1.assigned_ep, n2.assigned_ep)
                                    # 			(ecount1,ecount2) = (n1.assigned_ep.ecount,n2.assigned_ep.ecount)
                                    # 			n1.unbond()
                                    # 			rc=random.choice([True,False])
                                    # 			if (redox_zone==1) or (redox_zone==0 and rc):
                                    # 				print("reduction")
                                    # 				if ecount1 == 1:
                                    # 					ecount1 = 2
                                    # 				else:
                                    # 					if ecount1 == 0:
                                    # 						ecount1 = 1
                                    # 					if ecount2 ==0:
                                    # 						ecount2 = 1
                                    # 			if (redox_zone==2) or (redox_zone==0 and not rc):
                                    # 				print("oxidation")
                                    # 				if ecount1 == 1:
                                    # 					ecount1 = 0	
                                    # 				else:
                                    # 					if ecount2 ==2:
                                    # 						ecount2 = 1
                                    # 					if ecount1 == 2:
                                    # 						ecount1 = 1
                                    # 			(ep1.ecount,ep2.ecount) = (ecount1,ecount2)
                                    # 			self.np_q[i] = atom_i.calculate_q()
                                    # 			self.np_q[j] = atom_j.calculate_q()
