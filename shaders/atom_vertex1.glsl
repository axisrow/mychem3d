#version 430 

struct Node {
    vec4 pos;
    float q;
    float bonded;
    float pair;
    float noname;
};

struct Atom
{
    vec4 pos;
    vec4 v;
//    vec4 a;
    float type;
    float r;
    float m;
    float ncount;
    vec4 rot;
    vec4 rotv;
    Node nodes[5];
    vec4 color;
};



layout(std430, binding=0) buffer atoms_in
{
    Atom atoms[];
} In;

//layout(std430, binding=0) buffer atoms_in


layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform vec3 objectColor;
uniform int mode;
uniform int nodeindex;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out AtomData {
    Atom out_a;
};

//out vec4 atom_position;
out vec3 Normal;
out vec3 ObjectColor;
out vec3 FragPos;  

//out Atom currentAtom;


vec4 qmul(vec4 q1, vec4 q2)
{
         return vec4(
             q2.xyz * q1.w + q1.xyz * q2.w + cross(q1.xyz, q2.xyz),
             q1.w * q2.w - dot(q1.xyz, q2.xyz)
         );
}
   
// Vector rotation with a quaternion
// http://mathworld.wolfram.com/Quaternion.html
vec3 rotate_vector(vec3 v, vec4 r)
{
         vec4 r_c = r * vec4(-1, -1, -1, 1);
         return qmul(r, qmul(vec4(v, 0), r_c)).xyz;
}


void main()
{
    if (mode==0){  //vbo merge atoms and nodes 
//        float factor = 0.001;
        gl_Position = projection * view * model * vec4(position, 1.0f);
        ObjectColor = objectColor;
        FragPos = vec3(model * vec4(position, 1.0f));
        Normal = normal;
    }
    if (mode==1){ //ssbo atoms
        bool bug = false; 
        float factor = 0.001;
        Atom currentAtom = In.atoms[gl_InstanceID];
//        mat4 model = mat4( factor,  0,  0, 0,
//                           0,  factor, 0,  0 ,
//                           0,   0, factor,  0,
//                           currentAtom.pos.x,  currentAtom.pos.y  ,  currentAtom.pos.z ,    1  
//                           );

        vec4 vposition = vec4(position * currentAtom.r * factor +  currentAtom.pos.xyz*factor, 1.0f) ;
        //atom_position = currentAtom.pos*factor;
        gl_Position = projection * view * vposition;
//        if (currentAtom.pos.x != 515.0){
//            bug = true;
//        }
        ObjectColor = currentAtom.color.xyz;
        if (bug){
            ObjectColor = vec3(1,0,0);
        }
        FragPos = vposition.xyz;
        Normal = normal;
    }
    if (mode==2) { //nodes
        float factor = 0.001;
        Atom currentAtom = In.atoms[gl_InstanceID];
        vec3 nodepos = rotate_vector(currentAtom.nodes[nodeindex].pos.xyz, currentAtom.rot);
        nodepos += currentAtom.pos.xyz;
        vec4 vposition = vec4(position * 1 * factor +  nodepos*factor, 1.0f) ;
        gl_Position = projection * view * vposition;
        float q = currentAtom.nodes[nodeindex].q;
        float bonded = currentAtom.nodes[nodeindex].bonded;
        if (q==0) ObjectColor = vec3(1,1,1);
        if (q==1) ObjectColor = vec3(1,0,0); //vec3(255/256.0,95/256.0,160/256.0);
        if (q==-1) ObjectColor = vec3(0.0,0,252/256.0);
        //if (bonded==1) ObjectColor = vec3(0,1,0);
        //else ObjectColor = vec3(1,1,1);
        FragPos = vposition.xyz;
        Normal = normal;
    }
}