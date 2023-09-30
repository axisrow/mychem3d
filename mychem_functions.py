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
     return vertices



def OnOff(b):
	if b: return "On"
	else: return "Off"


#def molecule_extend(space, a1, nn1, type, nn2=1):

#    node1=a1.nodes[nn1]
