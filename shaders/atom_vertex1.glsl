#version 430 

struct Node {
    vec4 pos;
    vec4 rpos;  //real position
    float q;
    float bonded;
    float pair;
    float spin;
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
    float animate;
    float q;
    vec4 color;
    Node nodes[5];
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
        if (currentAtom.animate>0) ObjectColor = vec3(0,1,0);
        FragPos = vposition.xyz;
        Normal = normal;
    }
    if (mode==2) { //nodes
        float factor = 0.001;
        Atom currentAtom = In.atoms[gl_InstanceID];
        //vec3 nodepos = rotate_vector(currentAtom.nodes[nodeindex].pos.xyz, currentAtom.rot);
        vec3 nodepos = currentAtom.nodes[nodeindex].rpos.xyz;
        nodepos += currentAtom.pos.xyz;
        vec4 vposition = vec4(position * 1 * factor +  nodepos*factor, 1.0f) ;
        gl_Position = projection * view * vposition;
        float q = currentAtom.nodes[nodeindex].q;
        float spin = currentAtom.nodes[nodeindex].spin;
        //float bonded = currentAtom.nodes[nodeindex].bonded;
        // node charge and spin color
        if (q==0){
            if (spin==1) ObjectColor = vec3(0.5,0.5,0.5); 
            if (spin==-1) ObjectColor = vec3(1.0,1.0,1.0);
        }
        else{
            if (q==1) ObjectColor = vec3(1.0,0.0,0.0); 
            if (q==-1) ObjectColor = vec3(0.0,0.0,252/256.0);
        }

        //if (bonded==1) ObjectColor= ObjectColor/2;
        //else ObjectColor = vec3(1,1,1);
        FragPos = vposition.xyz;
        Normal = normal;
    }
}