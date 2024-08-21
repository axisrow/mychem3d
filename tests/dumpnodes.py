import random
import sys,os
import glm
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom, Space
from math import *

def action1(space:Space):
    (x,y,z)=(500,500,500)
    global i0,i1,i2,i3,a1,a2,a3
    if space.t==2:    
        space.compute2atoms()
        print("qsd")
        for a in space.atoms:
                q1 = a.nodes[0].q
                q2 = a.nodes[1].q if len(a.nodes)>1  else 0
                q3 = a.nodes[2].q if len(a.nodes)>2  else 0
                q4 = a.nodes[3].q if len(a.nodes)>3  else 0
                r = glm.vec4(q1,q2,q3,q4)
                st = str(r)
                st = st.replace("  1,","1.0,")
                st = st.replace("  -1,","-1.0,")
                st = st.replace(" 0 )","0.0 )")
                st = st.replace(" 0,","0.0,")
                print(f'{st},')



App = mychemApp()
random.seed(1)
space = App.space
space.action = action1
#space.merge_from_file("examples/alcohol/cyclic/20.json",500,500,500);
space.merge_from_file("examples/aminoacids/phenylalanine.json",500,500,500);
print(len(space.atoms))
App.run()


print("pos type")
for a in space.atoms:
    postype = glm.vec4(a.pos-glm.vec3(500,500,500),a.type)
    st = str(postype)
    st = st.replace("  0,","0.0,")
    st = st.replace(" )",".0)")
    print(st, ",")

print("rotations")
for a in space.atoms:
    r = glm.vec4(a.rot.x,a.rot.y,a.rot.z,a.rot.w)
    st = str(r)
    st = st.replace("  0,","0.0,")
   
    print(f'{st},')

        


#space.appendatom(a3)      

#space.appendmixer(2)
#space.export = True
#space.stoptime = 0

#import glm
#vector = glm.vec3(1,0,0);
#rotmat = glm.rotate(glm.radians(-90), (0,0,1) )
#vector = rotmat * vector
#print(vector.to_tuple())


  