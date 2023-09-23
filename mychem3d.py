# -*- coding: utf-8 -*-
import tkinter as tk
import time

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
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Simulation", menu=sim_menu)
        examples_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.create_json_menu(examples_menu,"examples/")
        self.menu_bar.add_cascade(label="Examples", menu=examples_menu)

        self.root.config(menu=self.menu_bar)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "MyChem 3D"
        self.space = Space()
        self.init_menu()
        self.lastX = 300
        self.lastY = 300
        #self.root.bind("<KeyPress>", self.handle_keypress)
        #self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<space>", self.handle_space)
        self.root.bind("<Alt-r>", self.handle_reset)
        self.root.bind("<Button-2>", self.handle_mouseb2)
        self.root.bind("<B2-Motion>", self.handle_mouse2move)
        self.root.bind("<s>", self.handle_shake)
        self.root.bind("<b>", self.handle_bondlock)
        #self.root.bind("<FocusIn>"), self.handle_focusin
        self.root.bind("<MouseWheel>", self.handle_scroll)
        self.glframe = AppOgl(self.root, width=1024, height=600)
        self.pause = False
        self.glframe.pack(fill=tk.BOTH, expand=tk.YES)
        self.glframe.animate = 1  
        self.glframe.set_space(self.space)
        #   app.config(cursor="none")
        #app.after(100, app.printContext)
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.set('Ready')


    def run(self):
        self.resetdata = self.space.make_export()
        self.space.atoms2numpy()
        self.root.mainloop()

    def sim_run(self):
        self.space.atoms2numpy()
        self.pause = False
        self.glframe.pause = False
        self.status_bar.set("Running")

    def sim_pause(self):
        self.space.numpy2atoms()
        self.pause = True
        self.glframe.pause = True
        #self.status_bar.settime(self.t)
        #self.status_bar.setinfo("Number of atoms: "+str(len(self.atoms)))
        self.status_bar.set("Paused")

    def handle_space(self,event=None):
        if self.pause:
            self.sim_run()
        else:
            self.sim_pause()


    def handle_shake(self,event=None):
        if event:
            self.space.shake = not self.space.shake
        self.status_bar.set("Random shake is "+ OnOff(self.space.shake))


    def handle_bondlock(self,event=None):
        if event:
            self.space.bondlock = not self.space.bondlock
        self.status_bar.set("Bondlock is "+ OnOff(self.space.bondlock))


    def file_new(self,event=None):
        pass

    def file_open(self,event=None):
        pass

    def file_merge(self,event=None, path=None):
        self.sim_pause()
        if path:
            print(path)
            fileName=path
        else:
            fileName = tk.filedialog.askopenfilename(title="Select file", filetypes=(("JSON files", "*.json"), ("All Files", "*.*")))
            if not fileName:	
                return
        f =  open(fileName,"r")		
        self.space.merge_atoms = []
        mergedata = json.loads(f.read())
        self.recentdata = mergedata
        self.resetdata = mergedata 
        #self.merge_mode=True
        self.space.load_data(mergedata, merge=False)
        #self.canvas.configure(cursor="hand2")
        #self.status_bar.set("Merging mode")


    def file_merge_recent(self,event=None):
        pass

    def file_save(self,event=None):
        pass

    def file_exit(self,event=None):
        pass


    def handle_reset(self,event=None):
        if not self.resetdata:
            return
        self.file_new()
        self.space.load_data(self.resetdata)
        self.status_bar.set("Reset to previos loaded")

   
    #  def handle_keypress(self,event):
    #     if not event.keysym in self.keypressed:
    #         self.keypressed.append(event.keysym)

    #  def handle_keyrelease(self,event):
    #     if event.keysym in self.keypressed:
    #          self.keypressed.remove(event.keysym)

    def handle_mouseb2(self,event:tk.Event):
          self.lastX = event.x
          self.lastY = event.y

    def handle_mouse2move(self,event:tk.Event):
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
        print(f'yaw={self.glframe.yaw} pitch{self.glframe.pitch} pos={self.glframe.cameraPos}')

    #  def handle_focusin(self,event:tk.Event):
    #      pass
    #      #glfw.set_cursor_pos(300,300)
    #      #self.lastX = event.x
    #      #self.lastY = event.y
         
    def handle_scroll(self,event:tk.Event):
         cameraSpeed = 0.1
         if event.delta>0:
              self.glframe.cameraPos += cameraSpeed * self.glframe.cameraFront
         else:
              self.glframe.cameraPos -= cameraSpeed * self.glframe.cameraFront
    #         self.fov -=5
    #     if self.fov < 1:
    #          self.fov = 1
    #     if self.fov > 120:
    #          self.fov = 120

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

     

if __name__ == '__main__':
    mychemApp().run()
