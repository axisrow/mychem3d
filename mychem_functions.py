from math import sin, cos, pi
import numpy as np, glm

def create_sphere(radius, num_segments):
    vertex_data = []
    index_data = []
    normal_data = []

    for i in range(num_segments + 1):
        for j in range(num_segments + 1):
            theta = i * (2 * pi) / num_segments
            phi = j * pi / num_segments

            x = radius * sin(phi) * cos(theta)
            y = radius * sin(phi) * sin(theta)
            z = radius * cos(phi)

            vertex_data.append((x, y, z))
            normal_data.append(glm.normalize(glm.vec3(x,y,z)))

            if i < num_segments and j < num_segments:
                first = i * (num_segments + 1) + j
                second = first + num_segments + 1
                index_data.extend([first, second, first + 1, second, second + 1, first + 1])
    
    return vertex_data, index_data, normal_data


def make_sphere_vert(radius, segments):
    vertices = []
    vertex_data, index_data,normal_data = create_sphere(radius, segments)
    for i in index_data:
            vertices.extend(list(vertex_data[i]))
            vertices.extend(list(normal_data[i]))
    return vertices



from mychem_data import cube2_surfaces, cube2_vertices
def make_cube2():
     vertices = []
     for s in cube2_surfaces:
        for s2 in s:
            vertices.extend(list(cube2_vertices[s2]))
            vertices.extend([0,0,-1])
     return vertices



def OnOff(b):
	if b: return "On"
	else: return "Off"


#def molecule_extend(space, a1, nn1, type, nn2=1):

#    node1=a1.nodes[nn1]



def bond_atoms(a1, a2, ni1=-1, ni2=-1):
    bi1 = 0
    bi2 = 0
    if ni1==-1:
        for i in range(0, len(a1.nodes)):
            if not a1.nodes[i].bonded and a1.nodes[i].q==0 :
                bi1 = i
                break
        else: return False
    else:
       bi1 = ni1
    if ni2==-1:
        for i in range(0, len(a2.nodes)):
            if not a2.nodes[i].bonded and a2.nodes[i].q==0:
                bi2 = i
                break
        else: return False
    else:
       bi2 = ni2
    a1.nodes[bi1].q = -1
    a1.nodes[bi1].spin = -1
    a2.nodes[bi2].q = 1
    a2.nodes[bi2].spin = 1
    return True



class UndoStack:
    def __init__(self, limit=10):
        self.stack = []
        self.limit = limit

    def push(self, data):
        print("push to undostack")
        if len(self.stack) >= self.limit:
            self.stack.pop(0)  
        self.stack.append(data)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0
    
