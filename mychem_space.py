import os
import json
from math import sqrt,sin,cos,pi,acos
import numpy as np
import random
from mychem_atom import Atom
import glm
import tkinter as tk
import time

class Space:
    def __init__(self,width=1000,height=1000,depth=1000):
        self.gpu_compute =tk.BooleanVar()
        self.gpu_compute.set(True)
        self.pause = False
        self.ucounter = 0
        self.setSize(width,height,depth)
        self.debug = False
        self.ATOMRADIUS = 10
        self.BOND_KOEFF = 0.2
        self.BONDR = 4.0
        self.INTERACT_KOEFF= 1.0
        self.ROTA_KOEFF = 10
        self.REPULSION1 = -3
        self.REPULSION_KOEFF1 = 10
        self.REPULSION2 = 6
        self.REPULSION_KOEFF2= 0.4
        self.MASS_KOEFF = 5.0
        self.MAXVELOCITY = 1
        self.NEARDIST = 200.0   # near atoms buffering
        self.heat = 0.0
        self.t = -1
        self.stoptime = -1
        self.recordtime = 0
        self.recording = tk.BooleanVar()
        self.recording.set(False)
        self.atoms = []	
        self.g = 0.001
        self.newatom = None
        self.createtype=4
        self.createf = 0
        self.standard = True
        self.merge_atoms = []
        self.merge_rot = glm.quat()
        self.merge_center = glm.vec3(0,0,0)
        self.select_mode = 0
        self.selected_atoms = [] 
        self.gravity = tk.BooleanVar()
        self.gravity.set(False)
        self.shake= tk.BooleanVar()
        self.shake.set(False)
        self.SHAKE_KOEFF = 0.5
        self.competitive = True
        self.redox = tk.BooleanVar()
        self.redox.set(False)
        self.redox_rate = 1
        self.segmented_redox = True
        self.bondlock =tk.BooleanVar()
        self.bondlock.set(False)
        self.linear_field = False
        self.update_delta= 5
        self.show_q = False
        self.action = None
        self.fdata = open('data.txt',"w")

    def setSize(self, width,height,depth):
        self.WIDTH=width
        self.HEIGHT=height
        self.DEPTH=depth
        self.box = glm.vec3(self.WIDTH, self.HEIGHT, self.DEPTH)
        self.merge_pos = self.box/2


    def appendatom(self,a):
        a.space = self
        self.atoms.append(a)

    def appendmixer(self,n=1):
        for i in range(0,n):
            m = Atom(random.randint(1,self.WIDTH),random.randint(1,self.HEIGHT),random.randint(1,self.DEPTH),100,r=30)
            m.space = self
            m.v = glm.vec3(random.random(),random.random(),random.random())
            m.m = 100
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
            self.np_x[i]=atom_i.pos.x
            self.np_y[i]=atom_i.pos.y
            self.np_z[i]=atom_i.pos.z
            self.np_vx[i]=atom_i.v.x
            self.np_vy[i]=atom_i.v.y
            self.np_vz[i]=atom_i.v.z
            self.np_ax[i]=atom_i.a.x
            self.np_ay[i]=atom_i.a.y
            self.np_az[i]=atom_i.a.z
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
            atom_i.pos = glm.vec3(self.np_x[i],self.np_y[i],self.np_z[i])
            atom_i.v = glm.vec3(self.np_vx[i],self.np_vy[i],self.np_vz[i])
            #atom_i.ax=self.np_ax[i]
            #atom_i.ay=self.np_ay[i]
            #atom_i.az=self.np_az[i]
            #atom_i.q=self.np_q[i]
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
         #print("center=",center)
         return center


    def get_atoms_center(self, atoms=None):
         if atoms==None:
            atoms = self.atoms
         sum = glm.vec3(0,0,0)
         N = len(atoms)
         for a in atoms:
              sum += a.pos
         center = sum/N
         return center


    def get_atoms_distant(self,atoms=None):
         if atoms==None:
              atoms = self.atoms
         center = self.get_atoms_center(atoms)
         distant = glm.vec3(0,0,0)
         N = len(atoms)
         for a in atoms:
              if abs(a.pos.x-center.x) > distant.x:
                   distant.x = a.pos.x-center.x
              if abs(a.pos.y-center.y) > distant.y:
                   distant.y = a.pos.y-center.y
              if abs(a.pos.z-center.z) > distant.z:
                   distant.z = a.pos.z-center.z
         return (center,distant)

    def get_node_by_index(self,index):
         index = int(index)
         if index==-1:
            return None
         ai = index//5
         ni = index%5
         #print(f"  for index{index} result = { ai}  {ni}")
         return self.atoms[ai].nodes[ni]
    
    def get_index_by_node(self,n):
        if n != None:
            parentindex = self.atoms.index(n.parent)
            nodeindex = n.parent.nodes.index(n)
            index = parentindex*5+nodeindex
            #print(f"node = {n} parentIndex={parentindex} nodeindex={nodeindex}")
        else:
            index = -1
        return index
         

    def atoms2compute(self):
        t = time.time()
        if self.gpu_compute.get():
            print("atoms2compute gpu")
            self.glframe.atoms2ssbo()
        else:
            print("atoms2compute numpy")
            self.glframe.atoms2ssbo()
            self.atoms2numpy()
        delta = time.time() - t
        print("  delta=", delta)            

    
    def compute2atoms(self):
        t = time.time()
        if self.gpu_compute.get():
            print("compute2atoms gpu")
            self.glframe.ssbo2atoms()
        else:
            print("compute2atoms numpy")
            self.numpy2atoms()
        delta = time.time() - t
        print("  delta=", delta)     

    def merge2atoms(self):
        #self.compute2atoms()
        N = len(self.atoms)
        self.merge_center = self.get_mergeobject_center()
        for a in self.merge_atoms:
            pos = a.pos.xyz
            pos -= self.merge_center
            pos = self.merge_rot * pos
            pos += self.merge_pos
            a.pos = pos.xyz
            a.rot = glm.normalize(self.merge_rot * a.rot)
            a.calc_node_positions()
            self.appendatom(a)
        self.merge_atoms = []
        return N
        #self.atoms2compute()


    def merge_from_file(self, filename, x=0,y=0,z=0, merge_rot=glm.quat()):
        f =  open(filename,"r")		
        self.merge_atoms = []
        mergedata = json.loads(f.read())
        self.load_data(mergedata, merge=True)
        self.merge_pos = glm.vec3(x,y,z)
        self.merge_rot = merge_rot
        first = self.merge2atoms()
        self.merge_pos = self.box/2
        self.merge_rot = glm.quat()
        return first
    
    def autospinset(self, atoms):
        N = len(atoms)
        print("Autospinset start")
        for i in range(0,N):
            atom_i = atoms[i]
            for j in range(0,N):
                if i==j: continue
                atom_j = atoms[j]
                for ni in range (0,len(atom_i.nodes)):
                    node_i = atom_i.nodes[ni]
                    if node_i.spin == 0:
                        ni_realpos =  atom_i.rot * node_i.pos
                        for nj in range(0, len(atom_j.nodes)):
                            node_j = atom_j.nodes[nj]
                            nj_realpos =  atom_j.rot * node_j.pos
                            rn = glm.distance(atom_i.pos + ni_realpos, atom_j.pos + nj_realpos)
                            if rn<self.BONDR:
                                if node_j.spin !=0:
                                    node_i.spin = - node_j.spin
                                else:
                                    node_i.spin = random.choice([-1,1])    
                    #print(f"spinset i={i} j={j} ni={ni} spin = {node_i.spin}" )                                    
        for i in range(0,N):
            atom_i = atoms[i]
            for ni in range (0,len(atom_i.nodes)):
                node_i = atom_i.nodes[ni]
                if node_i.spin == 0:
                    node_i.spin = random.choice([-1,1])    

        print("Autospinset stop")


         
    

    def shift_q(self,type1,type2, q1, q2):
        etable=[5,500,1,4,400,6,600,3,2,200]
        i1 = etable.index(type1)
        i2 = etable.index(type2)
        if (i1>i2):
            if (q1== 0 and q2== 0 ): return 1,-1,1
            if (q1== 0 and q2==-1 ): return 0,-1,0  
            if (q1== 0 and q2== 1 ): return 0,0,1  
            if (q1==-1 and q2== 0 ): return 0,-1,0
            if (q1==-1 and q2==-1 ): return 0,-1,-1
            if (q1==-1 and q2== 1 ): return 1,-1,1
            if (q1== 1 and q2== 0 ): return 0,0,1
            if (q1== 1 and q2==-1 ): return 1,-1,1
            if (q1== 1 and q2== 1 ): return 0,1,1
        if (i1==i2):
            if (q1+q2==0): return 1,0,0
            else: return 0,q1,q2
        if (i1<i2):
            if (q1== 0 and q2== 0 ): return 1,1,-1  
            if (q1== 0 and q2==-1 ): return 0,0,-1
            if (q1== 0 and q2== 1 ): return 0,1,0  
            if (q1==-1 and q2== 0 ): return 0,0,-1
            if (q1==-1 and q2==-1 ): return 0,-1,-1
            if (q1==-1 and q2== 1 ): return 1,1,-1  
            if (q1== 1 and q2== 0 ): return 0,1,0  
            if (q1== 1 and q2==-1 ): return 1,1,-1
            if (q1== 1 and q2== 1 ): return 0,1,1  


    def compute(self):
            N = len(self.atoms)
#            if N==0:
#                return 0
#            self.t +=1
            if self.stoptime!= -1:
                if self.t>self.stoptime:
                    return 0
            a = np.zeros((N,N))
            delta_x = np.subtract.outer(self.np_x, self.np_x)
            delta_y = np.subtract.outer(self.np_y, self.np_y)
            delta_z = np.subtract.outer(self.np_z, self.np_z)
            r2 = delta_x*delta_x + delta_y*delta_y + delta_z*delta_z
            r = np.sqrt(r2)
            r_reciproc = np.reciprocal(r,where=r!=0)
            a[r<self.np_SUMRADIUS_D2] = (r_reciproc*self.REPULSION_KOEFF2)[r<self.np_SUMRADIUS_D2]
            a[r<self.np_SUMRADIUS_D1] = (r_reciproc*self.REPULSION_KOEFF1)[r<self.np_SUMRADIUS_D1]
#            if self.competitive:
#                        Q = np.outer(self.np_q, self.np_q)
                        #if self.linear_field:
                            #a+= Q*self.INTERACT_KOEFF*0.1
                        #else:
                            #a += np.divide(Q,r,where=r!=0)*self.INTERACT_KOEFF
#                        if self.debug: 
#                            print(f"a={a} \nq={Q}")
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
                jj = np.where(np.logical_and(r[i]>0,r[i]<100))
                #print("jj=", jj)
                
                allnE = glm.vec3(0,0,0)
                for j in jj[0]:
                    if j==i: continue
                    atom_i = self.atoms[i]
                    atom_j = self.atoms[j]
                    for ni in range (0,len(atom_i.nodes)):
                        node_i = atom_i.nodes[ni]
                        ni_index= i*5+ni
                        ni_realpos =  self.np_rot[i] * node_i.pos
                        nE = glm.vec3(0,0,0)
                        for nj in range(0, len(atom_j.nodes)):
                            node_j = atom_j.nodes[nj]
                            nj_realpos =  self.np_rot[int(j)] * node_j.pos
                            nj_index = j*5+nj
                            ndelta = ni_realpos - nj_realpos + glm.vec3(self.np_x[i] - self.np_x[j], self.np_y[i] - self.np_y[j], self.np_z[i] - self.np_z[j] )
                            rn = glm.length(ndelta)
                            #if rn==0: continue
                            a = 0
                            if rn<=self.BONDR and not node_i.bonded and not node_j.bonded:
                                    if self.debug: print("bond")
                                    bonded,node_i.q,node_j.q = self.shift_q(atom_i.type, atom_j.type, node_i.q,node_j.q)
                                    if bonded:
                                        node_i.bond(node_j)
                                        #node_i.bonded = True
                                        #node_i.pair = node_j
                                        #node_j.bonded = True
                                        #node_j.pair = node_i
                            if rn>self.BONDR and node_i.bonded and node_j.bonded and node_i.pair==node_j:
                                 if self.debug: print("unbond")
                                 node_i.unbond()
                                 #node_i.bonded = False
                                 #node_i.pair = None
                                 #node_j.bonded = False
                                 #node_j.pair = None
                            
                            if rn<=self.BONDR and node_i.bonded and node_j.bonded and  node_i.pair==node_j:
                                        a = -rn*self.BOND_KOEFF  #atom's bond force
                                        if node_i.q+node_j.q !=0 and not self.bondlock.get():
                                             if self.debug: print("unbond2")
                                             node_i.unbond()
                                             #node_i.bonded = False
                                             #node_i.pair = None
                            elif rn>self.BONDR and not node_i.bonded and not node_j.bonded and self.t>1:
                                    if rn!=0: a= node_i.q*node_j.q*self.INTERACT_KOEFF/rn
                                    #if self.debug: print(a)
                                    pass

                            #if i==0 and ni==atom_i.nodes[0]:
                            #    self.fdata.write(f"t = {self.t} {a:0.5f} rn={rn:0.4f} v={self.np_vx[i]:0.2f} {self.np_vy[i]:0.2f} {self.np_vz[i]:0.2f} \n")
 
                            target_direction = nj_realpos - glm.vec3(self.np_x[i] - self.np_x[j], self.np_y[i] - self.np_y[j], self.np_z[i] - self.np_z[j] )
                            v1 = glm.normalize(ni_realpos)
                            v2 = glm.normalize(target_direction)
                            dt = glm.dot(v1,v2)
                            if dt>1: dt=1
                            if dt<-1: dt=-1
                            if v1!=v2:
                                axis = glm.cross(v1,v2)
                                angle = acos(dt)
                                angle_a= -angle*a*self.ROTA_KOEFF
                                rot = glm.quat(cos(angle_a/2), sin(angle_a/2)*glm.vec3(axis))
                                totalrotv = glm.normalize(rot * totalrotv)
                                #naf2=0
                                #if self.debug: print(f"axis={axis} angle={angle} dt={dt}")
                            if rn!=0: nE+= ndelta/rn*a
                        allnE = allnE + nE
                self.np_rotv[i] = totalrotv #* self.np_rotv[i]
                Ex[i] += allnE.x
                Ey[i] += allnE.y
                Ez[i] += allnE.z
                #if self.debug: print("##")
            self.np_ax= Ex/self.np_m
            self.np_ay= Ey/self.np_m
            self.np_az= Ez/self.np_m
            #print(self.np_az)


            if self.gravity.get():
                self.np_ay -= self.g

            if self.shake.get():
                self.np_ax += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)
                self.np_ay += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)
                self.np_az += self.SHAKE_KOEFF * (np.random.rand(N)-0.5)

            #set mixers velocity		
            #if len(self.mixers)>0:
            #self.np_vx[np.logical_and(self.np_type==100,self.np_vx>=0)] = 1
            #self.np_vx[np.logical_and(self.np_type==100,self.np_vx<0)] = -1
            #self.np_vy[np.logical_and(self.np_type==100,self.np_vy>=0)] = 1
            #self.np_vy[np.logical_and(self.np_type==100,self.np_vy<0)] = -1
            #self.np_vz[np.logical_and(self.np_type==100,self.np_vz>=0)] = 1
            #self.np_vz[np.logical_and(self.np_type==100,self.np_vz<0)] = -1

            self.np_next()
            self.np_limits()
            
            
            if self.action:
                self.action(self)            
            return N


    def make_export(self):
        frame = {}
        frame["vers"] = "1.0"
        frame["time"] = self.t
        frame["atoms"] = []
        N = len(self.atoms)
        for i in range(0,N):
            if self.atoms[i].color == (0,0,0): continue    #spec color for remove atoms on save
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
            atom["nodes"] = []
            for n in self.atoms[i].nodes:
                 node ={}
                 node["q"]=n.q
                 atom["nodes"].append(node)
                 
            frame["atoms"].append(atom)
        return frame

    def load_data(self, j, merge=False, zerospeed=True):
        if not merge: 
            self.atoms = []
        for a in j["atoms"]:
            type = a["type"]
            #if type==100: continue
            if "z" in a:
                z = a["z"]
                vz = a["vz"]
                rot = glm.quat(a["rot"])
            else:
                z = 500
                vz = 0
                if type==4: type=400
                if type==2: type=200
                if type==5: type=500
                if type==6: type=600
                rot = glm.quat(glm.vec3(0,0,-a["f"]))
            aa = Atom(a["x"],a["y"],z, type=type, r=a["r"] )
            if zerospeed and type!=100:
                aa.v= glm.vec3(0,0,0) 
            else:
                aa.v = glm.vec3(a["vx"],a["vy"],vz)
            aa.rot = rot
            aa.calc_node_positions()
            aa.q=a["q"]
            aa.m=a["m"]
#            if not "version" in j:
#                 aa.f= 2*pi - aa.f
            ni = 0
            if "nodes" in a:
                 for n in a["nodes"]:
                    aa.nodes[ni].q= n["q"]
                    ni+=1
            if merge:
                aa.space = self
                self.merge_atoms.append(aa)
            else:
                self.appendatom(aa)
        if merge:
            self.autospinset(self.merge_atoms)			
        else:
            self.autospinset(self.atoms)    



