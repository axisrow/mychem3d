Pseudochemical 3d simulator
- python tkinter used
- opengl 4.3 with compute shader used for parallel computation
- not release by now

for use install libraries:
- python -m pip install pillow numpy pyglm pyopengl pyopengltk

Tested on:
- integrated Intel Iris Xe Graphics

Be careful. This application may create misconceptions about chemical interactions

Controls:
-    Mouse + left button  -  rotate camera
-    Mouse + right button - move camera left and right
-     +shift - gently
-    Mouse wheel - move camera forward and back

 In merge mode (adding atoms or files):
- enter or click - do merge 
- mouse wheel - change parameter
- mouse wheel + shift - slow change
- mouse wheel + control - move camera forward and back
- g - move,  x,y,z for select axis
- r - rotate object, x,y,z for select rotate axis

Selection atoms
1. molecule selection mode
  -  click an atom, then use the mouse wheel to add neighboring atoms to the selection
  -  ctrl + click  - append/remove to/from selection
  -  enter or click on selection - go to merge mode with selected atoms
  -  also "r" and "g" - go to merge mode with move and rotation
  -  <delete> - delete selected
  -  ctrl + alt + s - save selected atoms
  -  "b" - try to bond two selected atoms with selected nodes, resutl in statusbar
  -   middle button for change selected node in selected atom




Do not watch video parallel to runing this simulator or iconize it, the simulation may hang


Some examples:

!["demopic 1](images/demo1.PNG?raw=true )
!["demopic 2](images/demo2.JPG?raw=true )

