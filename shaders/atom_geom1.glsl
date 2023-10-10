#version 430 

layout (points) in;
//layout (points) out;
layout (triangle_strip, max_vertices = 256) out;





layout(std430, binding=2) buffer SphereData
{
   vec3 sphere_data[];
};

in Atom currentAtom[];
in vec4 atom_position[];

out vec3 ObjectColor;
out vec3 Normal;
out vec3 FragPos;

void main() {
 
    for (int si =0; si< sphere_data.length()/2;si++){
        if (si%3==0 && si>0) EndPrimitive();
        ObjectColor = vec3(1,1,1);
        FragPos =  atom_position[0].xyz;
        //gl_Position =  projection * (atom_position[0] + vec4(sphere[si].pos, 1.0));
        //gl_Position =  projection * (atom_position[0] + vec4(sphere[si].pos, 1.0));
        gl_Position =  atom_position[0] +  vec4(sphere_data[si*2]*0.1, 1.0);
        EmitVertex();
    }
}