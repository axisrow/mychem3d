# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.filedialog as filedialog
import time
from math import sin,cos,log
import os
import json
from json import encoder
from PIL import ImageGrab
from mychem_atom import Atom
from mychem_space import Space
from mychem_gl import AppOgl
from mychem_functions import OnOff
import glm

class mychemApp():
    def init_menu(self):
        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New", accelerator="Alt+n",command=self.file_new)
        file_menu.add_command(label="Open", accelerator="o", command=self.file_open)
        file_menu.add_command(label="Merge", accelerator="m", command=self.file_merge)
        file_menu.add_command(label="Merge recent", accelerator="l", command=self.file_merge_recent)
        file_menu.add_command(label="Save", accelerator="Alt+s", command=self.file_save)
        file_menu.add_command(label="Exit", command=self.file_exit)
        sim_menu = tk.Menu(self.menu_bar, tearoff=False)
        sim_menu.add_command(label="Go/Pause", accelerator="Space",command=self.handle_space)
        sim_menu.add_command(label="Reset", accelerator="Alt+r",command=self.handle_reset)
        sim_menu.add_checkbutton(label="Random shake", accelerator="s",command=self.handle_shake)
        sim_menu.add_checkbutton(label="Bond lock", accelerator="b", variable=self.space.bondlock, command=self.handle_bondlock)
        sim_menu.add_checkbutton(label="Two zone redox", accelerator="r", variable=self.space.redox,command=self.handle_redox)
        sim_menu.add_checkbutton(label="Recording",variable=self.space.recording, command=self.handle_recording)
        add_menu = tk.Menu(self.menu_bar, tearoff=False)
        add_menu.add_command(label="H", accelerator="1",command=lambda:self.handle_add_atom(keysym="1"))
        add_menu.add_command(label="O", accelerator="2",command=lambda:self.handle_add_atom(keysym="2"))
        add_menu.add_command(label="N", accelerator="3",command=lambda:self.handle_add_atom(keysym="3"))
        add_menu.add_command(label="C", accelerator="4",command=lambda:self.handle_add_atom(keysym="4"))
        add_menu.add_command(label="P", accelerator="5",command=lambda:self.handle_add_atom(keysym="5"))
        add_menu.add_command(label="S", accelerator="6",command=lambda:self.handle_add_atom(keysym="6"))        
        add_menu.add_command(label="Mixer", accelerator="0",command=lambda:self.handle_zero())
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Simulation", menu=sim_menu)
        self.menu_bar.add_cascade(label="Add", menu=add_menu)
        self.menu_bar.add_command(label="Options", command=self.options_window)
        examples_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.create_json_menu(examples_menu,"examples/")
        self.menu_bar.add_cascade(label="Examples", menu=examples_menu)
        self.root.config(menu=self.menu_bar)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MyChem 3D")
        self.space = Space()
        self.init_menu()
        self.lastX = 300
        self.lastY = 300
        self.root.bind("1", self.handle_add_atom2)
        self.root.bind("2", self.handle_add_atom2)
        self.root.bind("3", self.handle_add_atom2)
        self.root.bind("4", self.handle_add_atom2)
        self.root.bind("5", self.handle_add_atom2)
        self.root.bind("6", self.handle_add_atom2)
        self.root.bind("<Left>", self.handle_cursor)
        self.root.bind("<Right>", self.handle_cursor)
        #self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<space>", self.handle_space)
        self.root.bind("<Alt-r>", self.handle_reset)
        self.root.bind("<Alt-n>", self.file_new)
        self.root.bind("<Alt-o>", self.file_open)
        self.root.bind("<Alt-s>", self.file_save)
        self.root.bind("<Button-1>", self.handle_mouseb1)
        self.root.bind("<Return>", self.handle_enter)
        self.root.bind("<Escape>", self.handle_escape)
        self.root.bind("<B1-Motion>", self.handle_mouse1move)
        self.root.bind("<Motion>", self.handle_motion)
        self.root.bind("<Double-Button-1>", self.handle_doubleclick)
        self.root.bind("<s>", self.handle_shake)
        self.root.bind("x", self.handle_mode)
        self.root.bind("y", self.handle_mode)
        self.root.bind("z", self.handle_mode)
        self.root.bind("r", self.handle_mode)
        self.root.bind("g", self.handle_mode)
        self.root.bind("l", self.file_merge_recent)
        self.root.bind("<Alt-g>", self.handle_g)
        self.root.bind("0", self.handle_zero)
        self.root.bind("<b>", self.handle_bondlock)
        #self.root.bind("<FocusIn>"), self.handle_focusin
        self.root.bind("<MouseWheel>", self.handle_scroll)
        self.glframe = AppOgl(self.root, width=1024, height=600)
        print("glframe created")
        self.pause = False
        self.merge_mode = False
        self.ttype = "mx"
        self.glframe.pack(fill=tk.BOTH, expand=tk.YES)
        self.glframe.animate = 1  
        self.glframe.set_space(self.space)
        #   app.config(cursor="none")
        #app.after(100, app.printContext)
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        if not os.path.exists('output'):
            os.makedirs('output')

        self.status_bar.set('Ready')

    def run(self):
        self.resetdata = self.space.make_export()
        #self.atoms2compute()
        self.root.mainloop()


    def sim_run(self):
        #self.atoms2compute()
        #self.atoms2compute()
        self.pause = False
        self.glframe.pause = False
        #self.glframe.animate = 1
        self.status_bar.set("Running")

    def sim_pause(self):
        self.compute2atoms()
        self.pause = True
        self.glframe.pause = True
        #self.glframe.animate = 0
        self.status_bar.settime(self.glframe.nframes)
        self.status_bar.setinfo("Number of atoms: "+str(len(self.space.atoms)))
        self.status_bar.set("Paused")

    def handle_recording(self,event=None):
        if event:
            self.space.recording.set(not self.space.recording.get())
        self.status_bar.set("Recording frames to disk is "+ OnOff(self.space.recording))
        
    def handle_space(self,event=None):
        if self.pause:
            self.sim_run()
        else:
            self.sim_pause()


    def handle_mode(self,event=None):
        if not self.merge_mode: return
        if event.keysym == "r":
           self.ttype = "r" + self.ttype[1]
           self.status_bar.set("Rotate "+ self.ttype[1] )
           return
        if event.keysym == "g":
           self.ttype ="m" + self.ttype[1]
           self.status_bar.set("Move "+ self.ttype[1] )
           return
        self.ttype=self.ttype[0]
        if event.keysym == "x":
            self.ttype+="x"
        if event.keysym == "y":
            self.ttype+="y"
        if event.keysym == "z":
            self.ttype+="z"
        if self.ttype[0]=="r":
            self.status_bar.set("Rotate "+ self.ttype[1] )
        else:
            self.status_bar.set("Move "+ self.ttype[1] )


    def handle_shake(self,event=None):
        if event:
            self.space.shake = not self.space.shake
        self.status_bar.set("Random shake is "+ OnOff(self.space.shake))

    def handle_redox(self,event=None):
        if event:
            self.space.redox.set(not self.space.redox.get())
        print(self.space.redox.get())
        self.status_bar.set("Two zone redox is "+ OnOff(self.space.redox.get()))

    def handle_g(self,event=None):
        if event:
            self.space.gravity.set(not self.space.gravity.get())
        self.status_bar.set("Gravity is "+ OnOff(self.space.gravity.get()))

    def handle_zero(self,event=None):
        #self.compute2atoms()
        self.space.appendmixer(1)
        self.resetdata = self.space.make_export()
        self.atoms2compute()


    def handle_bondlock(self,event=None):
        if event:
            self.space.bondlock.set(not self.space.bondlock.get())
        self.status_bar.set("Bondlock is "+ OnOff(self.space.bondlock.set()))


    def file_new(self,event=None):
        self.space.t = -1
#        self.recordtime = 0
        self.sim_pause()
        self.space.atoms = []	
        self.space.mixers = []
        self.space.merge_pos = glm.vec3(0,0,0)
        self.space.merge_rot = glm.quat()
        self.space.merge_atoms = []
        self.space.select_mode = False
        self.merge_mode = False
        self.atoms2compute()
        self.status_bar.set("New file")

    def file_open(self,event=None):
        fileName = filedialog.askopenfilename(title="Select file", filetypes=(("JSON files", "*.json"), ("All Files", "*.*")))
        if not fileName:	
            return
        self.file_new()
        f =  open(fileName,"r")		
        self.resetdata = json.loads(f.read())
        self.space.load_data(self.resetdata)
        self.atoms2compute()
        self.status_bar.set("File loaded")

    def file_merge(self,event=None, path=None):
        self.sim_pause()
        if path:
            print(path)
            fileName=path
        else:
            fileName = filedialog.askopenfilename(title="Select file", filetypes=(("JSON files", "*.json"), ("All Files", "*.*")))
            if not fileName:	
                return
        f =  open(fileName,"r")		
        self.space.merge_atoms = []
        mergedata = json.loads(f.read())
        self.recentdata = mergedata
        #self.resetdata = mergedata 
        self.merge_mode=True
        self.space.select_mode = False
        self.space.load_data(mergedata, merge=True)
        self.space.merge_center = self.space.get_mergeobject_center()
        #self.atoms2compute()
        #self.canvas.configure(cursor="hand2")
        self.status_bar.set("Merging mode")


    def file_merge_recent(self,event=None):
        if not self.recentdata:
            return
        self.sim_pause()
        self.merge_atoms = []
        self.merge_mode=True
        self.space.load_data(self.recentdata, merge=True)
        #self.atoms2compute()
        self.space.merge_center = self.space.get_mergeobject_center()
        self.status_bar.set("Merging mode")

    def file_save(self,event=None):
        self.sim_pause()
        fileName = tk.filedialog.asksaveasfilename(title="Save As", filetypes=(("JSON files", "*.json"), ("All Files", "*.*")))
        if not (fileName.endswith(".json") or fileName.endswith(".JSON")):
            fileName+=".json"
        f = open(fileName, "w")
        self.resetdata = self.space.make_export()
        f.write(json.dumps(self.resetdata))
        f.close()
        self.status_bar.set("File saved")

    def file_exit(self,event=None):
        pass

    def handle_cursor(self,event=None):
        if self.merge_mode == True: return
        self.space.select_mode = True
        N = self.space.np_x.size
        if event.keysym == "Left":
            self.space.select_i -=1
            if self.space.select_i < 0:
                self.space.select_i=N-1
        if event.keysym == "Right":
            self.space.select_i +=1
            if self.space.select_i >=N:
                self.space.select_i =0

    def handle_reset(self,event=None):
        if not self.resetdata:
            return
        self.file_new()
        self.space.load_data(self.resetdata)
        self.atoms2compute()
        self.status_bar.set("Reset to previos loaded")
    
    def handle_add_atom2(self,event=None):
        self.handle_add_atom(keysym=event.keysym)

    def handle_add_atom(self,keysym=""):
        self.sim_pause()
        self.space.merge_pos.x +=25
        self.merge_mode = True
        self.ttype = "mx"
        if keysym in ["1","2","3","4","5","6"]:
            createtype = int(keysym)
            a = Atom(500,500,500,createtype)
        self.space.merge_atoms = [a]
        self.space.merge_center = self.space.get_mergeobject_center()    
        
         #if not event.keysym in self.keypressed:
         #    self.keypressed.append(event.keysym)

    # def handle_keyrelease(self,event):
    #     if event.keysym in self.keypressed:
    #          self.keypressed.remove(event.keysym)

    def handle_escape(self,event):
        if self.merge_mode:
            self.merge_mode = False
            self.space.merge_atoms = []

    def handle_doubleclick(self,event):
        if self.merge_mode:
            self.handle_enter(event)
            return
        #(x,y,z) = glm.unProject(glm.vec3(event.x,event.y,0),self.glframe.view,self.glframe.projection, (0,0,self.glframe.width,self.glframe.height))
        #print(x,y,z)

        
    def handle_enter(self,event:tk.Event):
        if self.space.select_mode:
            self.sim_pause()
            a = self.space.atoms[self.space.select_i]
            self.space.merge_atoms = [a]
            self.space.merge_pos = glm.vec3(0,0,0)
            self.space.merge_rot = glm.quat()
            self.space.atoms.remove(a)
            self.space.merge_center = self.space.get_mergeobject_center()
            self.merge_mode = True
            
            self.space.select_mode = False
            self.atoms2compute()
            return
        if self.merge_mode:
            self.merge_mode = False 
            self.space.merge2atoms()
            self.resetdata = self.space.make_export()
            self.atoms2compute()



    def handle_mouseb1(self,event:tk.Event):
        self.lastX = event.x
        self.lastY = event.y
            
        

    def handle_mouse1move(self,event:tk.Event):
        shift = event.state & 1

        offsetx = event.x - self.lastX 
        offsety = event.y - self.lastY
        self.lastX = event.x
        self.lastY = event.y
        sense = 0.1
        offsetx *= sense
        offsety *= sense
        if shift:
            self.glframe.cameraPos -= glm.normalize(glm.cross(self.glframe.cameraFront, self.glframe.cameraUp)) * offsetx*0.05
            self.glframe.cameraPos += self.glframe.cameraUp * offsety*0.05
        else:
            self.glframe.pitch -=offsety
            self.glframe.yaw += offsetx
            if self.glframe.pitch > 89:
                self.glframe.pitch = 89
            if self.glframe.pitch < -89:
                self.glframe.pitch = -89
        #print(f'yaw={self.glframe.yaw} pitch{self.glframe.pitch} pos={self.glframe.cameraPos}')


    def handle_motion(self,event:tk.Event):
        shift = event.state & 1
        offsetx = event.x - self.lastX 
        offsety = event.y - self.lastY
        self.lastX = event.x
        self.lastY = event.y
        if shift:
            sense = 0.1
        else:
            sense = 0.5
        offsetx *= sense
        offsety *= sense


    def handle_scroll(self,event:tk.Event):
         shift = event.state & 1
         ctrl = event.state & 4
         if self.merge_mode and not ctrl:
            if not shift:
                offset = 15
                angle = 5
            else:
                offset = 1
                angle = 1
            if event.delta>0:
                angle*=-1
                offset*=-1
            if self.ttype=="mx":
                self.space.merge_pos.x -=offset
            if self.ttype=="my":
                self.space.merge_pos.y -=offset
            if self.ttype=="mz":
                self.space.merge_pos.z -=offset
            if self.ttype=="rx":
                self.space.merge_rot = glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*glm.vec3(1,0,0)) * self.space.merge_rot
            if self.ttype=="ry":
                self.space.merge_rot = glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*glm.vec3(0,1,0)) * self.space.merge_rot
            if self.ttype=="rz":
                self.space.merge_rot = glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*glm.vec3(0,0,1)) * self.space.merge_rot
         else:
            if shift:
                cameraSpeed = 0.01
            else:
                cameraSpeed = 0.1
            if event.delta>0:
                self.glframe.cameraPos += cameraSpeed * self.glframe.cameraFront
            else:
                self.glframe.cameraPos -= cameraSpeed * self.glframe.cameraFront   

    def atoms2compute(self):
        print("atoms2compute")
        if self.space.gpu_compute.get():
            self.glframe.atoms2ssbo()
        else:
            self.space.atoms2numpy()

    def compute2atoms(self):
        if self.space.gpu_compute.get():
            #self.glframe.atoms2ssbo()
            pass
        else:
            self.space.numpy2atoms()



    def create_json_menu(self,menu, lpath):
        files_last = []
        for filename in os.listdir(lpath):
            filepath = os.path.join(lpath, filename)
            if os.path.isdir(filepath):
                submenu = tk.Menu(menu,tearoff=False)
                menu.add_cascade(label=filename, menu=submenu)
                self.create_json_menu(submenu, filepath)
            elif os.path.splitext(filename)[-1] == ".json":
                files_last.append((filename,filepath))
        for (f,p) in files_last:				
            menu.add_command(label=f, command=lambda p2=p: self.file_merge(path=p2))

    def options_window(self):
        o = OptionsFrame(self.space)
        
    def about_window(self):
        
        a = tk.Toplevel()
        a.geometry('200x150')
        a['bg'] = 'grey'
        a.overrideredirect(True)
        tk.Label(a, text="About this")\
            .pack(expand=1)
        a.after(5000, lambda: a.destroy())



class StatusBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        status_frame = tk.Frame(parent, bd=1, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.label = tk.Label(status_frame, text= "Status")
        self.label.pack(side=tk.LEFT)
        self.timelabel = tk.Label(status_frame, text="Time")
        self.timelabel.pack(side=tk.RIGHT)
        self.info = tk.Label(status_frame, text="Info")
        self.info.pack(side=tk.RIGHT)

    
    def set(self, text):
        self.label.config(text=text)

    def settime(self,t):
        self.timelabel.config(text="Time:"+str(t))

    def setinfo(self,info):
        self.info.config(text=info)
    
    def clear(self):
        self.label.config(text='')


class OptionsFrame():
    def __init__(self,space):
        self.space = space
        a = tk.Toplevel()
        a.title("Options")
        a.resizable(0, 0)
        a.geometry('420x300')
        #self.frame = tk.Frame(a, bd=5, relief=tk.SUNKEN)
        #self.frame.pack()
        self.label0 = tk.Label(a, text= "Update delta").grid(row=0,column=0)
        self.update_slider = tk.Scale(a, from_=1, to=500, length=300, orient=tk.HORIZONTAL,command=self.set_delta)
        self.update_slider.grid(row=0,column=1)
        self.update_slider.set(self.space.update_delta)

        self.label1 = tk.Label(a, text= "Interact koeff").grid(row=1,column=0)
        self.interact_slider = tk.Scale(a, from_=1, to=500, length=300,orient=tk.HORIZONTAL,command=self.set_interk)
        self.interact_slider.grid(row=1,column=1)
        self.interact_slider.set(int(self.space.INTERACT_KOEFF*100))

        self.label2 = tk.Label(a, text= "Repulsion koeff1").grid(row=2,column=0)
        self.repulsek1_slider = tk.Scale(a, from_=1, to=500, length=200,orient=tk.HORIZONTAL,command=self.set_repulsek1)
        self.repulsek1_slider.grid(row=2,column=1)
        self.repulsek1_slider.set(int(self.space.REPULSION_KOEFF1))

        self.label3 = tk.Label(a, text= "Repulsion koeff2").grid(row=3,column=0)
        self.repulsek2_slider = tk.Scale(a, from_=1, to=500, length=300,orient=tk.HORIZONTAL,command=self.set_repulsek2)
        self.repulsek2_slider.grid(row=3,column=1)
        self.repulsek2_slider.set(self.space.REPULSION_KOEFF2*100)
        
        self.label4 = tk.Label(a, text= "Bond koeff").grid(row=4,column=0)
        self.bondk_slider = tk.Scale(a, from_=1, to=300, length=300,orient=tk.HORIZONTAL,command=self.set_bondk)
        self.bondk_slider.grid(row=4,column=1)
        self.bondk_slider.set(self.space.BOND_KOEFF*100)
        
        self.label5 = tk.Label(a, text= "Rotation koeff").grid(row=5,column=0)
        self.rotk_slider = tk.Scale(a, from_=1, to=100, length=100,orient=tk.HORIZONTAL,command=self.set_rotk)
        self.rotk_slider.grid(row=5,column=1)
        #self.rotk_slider.set( -log(self.space.ROTA_KOEFF,10))
        self.rotk_slider.set(self.space.ROTA_KOEFF*10)

        self.checkbox = tk.Checkbutton(a, text="GPU Compute", variable=self.space.gpu_compute,command=self.on_checkbox).grid(row=6,column=0)

        #checkbox = tk.Checkbutton(a, text="Show Q", variable=self.space.show_q).grid(row=4,column=0)

    def on_checkbox(self):
        print('on checkbox')
        if self.space.gpu_compute.get():
            self.glframe.atoms2ssbo()
        else:
            if len(self.space.atoms)>300:
                print("Too much atoms!")
                self.space.gpu_compute.set(True) 
            else:
                self.space.atoms2numpy()

    def set_delta(self,value):
        self.space.update_delta = int(value)

    def set_interk(self,value):
        self.space.INTERACT_KOEFF=float(value)/100.0

    def set_repulsek1(self,value):
        self.space.REPULSION_KOEFF1 =float(value)

    def set_repulsek2(self,value):
        self.space.REPULSION_KOEFF2=float(value)/100

    def set_bondk(self,value):
        self.space.BOND_KOEFF =float(value)/100

    def set_rotk(self,value):

        self.space.ROTA_KOEFF = float(value)/10.0
#        print("rota =",self.space.ROTA_KOEFF)



if __name__ == '__main__':
    mychemApp().run()
