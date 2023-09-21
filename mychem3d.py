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
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Simulation", menu=sim_menu)
        self.root.config(menu=self.menu_bar)

    def __init__(self):
        self.root = tk.Tk()
        self.init_menu()
        self.lastX = 300
        self.lastY = 300
        #self.root.bind("<KeyPress>", self.handle_keypress)
        #self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<Button-2>", self.handle_mouseb2)
        self.root.bind("<B2-Motion>", self.handle_mouse2move)
        #self.root.bind("<FocusIn>"), self.handle_focusin
        self.root.bind("<MouseWheel>", self.handle_scroll)
        self.glframe = AppOgl(self.root, width=1024, height=768)
        
        self.glframe.pack(fill=tk.BOTH, expand=tk.YES)
        self.glframe.animate = 1  
        self.space = Space()
        self.glframe.set_space(self.space)
        #   app.config(cursor="none")
        #app.after(100, app.printContext)
    
    def run(self):
        self.root.mainloop()


    def file_new(self,event=None):
        pass

    def file_open(self,event=None):
        pass

    def file_merge(self,event=None):
        pass

    def file_merge_recent(self,event=None):
        pass

    def file_save(self,event=None):
        pass

    def file_exit(self,event=None):
        pass

    def handle_space(self,event=None):
        pass

    def handle_reset(self,event=None):
        pass

   
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
            self.glframe.cameraPos -= glm.normalize(glm.cross(self.glframe.cameraFront, self.glframe.cameraUp)) * offsetx*0.01
          else:
            self.glframe.pitch -=offsety
            self.glframe.yaw += offsetx
            if self.glframe.pitch > 89:
                self.glframe.pitch = 89
            if self.glframe.pitch < -89:
                self.glframe.pitch = -89

    #  def handle_focusin(self,event:tk.Event):
    #      pass
    #      #glfw.set_cursor_pos(300,300)
    #      #self.lastX = event.x
    #      #self.lastY = event.y
         
    def handle_scroll(self,event:tk.Event):
         cameraSpeed = 30* self.glframe.framedelta
         if event.delta>0:
              self.glframe.cameraPos += cameraSpeed * self.glframe.cameraFront
         else:
              self.glframe.cameraPos -= cameraSpeed * self.glframe.cameraFront
    #         self.fov -=5
    #     if self.fov < 1:
    #          self.fov = 1
    #     if self.fov > 120:
    #          self.fov = 120
        


     

if __name__ == '__main__':
    mychemApp().run()
