#version 430 

struct Atom
{
    vec4 pos;
    vec4 v;
    vec4 a;
    float type;
    //mat4 rot;
    vec4 color;
};



layout(std430, binding=0) buffer atoms_in
{
    Atom atoms[];
} In;



layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform vec3 objectColor;
uniform int mode;
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
    if (mode==0){ 
//        float factor = 0.001;
        gl_Position = projection * view * model * vec4(position, 1.0f);
        ObjectColor = objectColor;
        FragPos = vec3(model * vec4(position, 1.0f));
        Normal = normal;
    }
    if (mode==1){
        bool bug = false; 
        float radius = 10;
        float factor = 0.001;
        Atom currentAtom = In.atoms[gl_InstanceID];
//        mat4 model = mat4( factor,  0,  0, 0,
//                           0,  factor, 0,  0 ,
//                           0,   0, factor,  0,
//                           currentAtom.pos.x,  currentAtom.pos.y  ,  currentAtom.pos.z ,    1  
//                           );

        vec4 vposition = vec4(position * radius * factor +  currentAtom.pos.xyz*factor, 1.0f) ;
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
    
}