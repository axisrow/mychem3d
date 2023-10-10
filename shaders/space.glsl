#version 430

// Set up our compute groups
layout(local_size_x=1, local_size_y=1) in;

// Input uniforms go here if you need them.
// Some examples:
//uniform vec2 screen_size;
//uniform vec2 force;
//uniform float frame_time;

// Structure of the ball data
struct Atom
{
    vec4 pos;
    vec4 v;
    vec4 a;
    float type;
    //mat4 rot;
    vec4 color;
};

// Input buffer
layout(std430, binding=0) buffer atoms_in
{
    Atom atoms[];
} In;

layout(std430, binding=1) buffer atoms_out
{
    Atom atoms[];
} Out;


int i = int(gl_GlobalInvocationID);
// Output buffer
//layout(std430, binding=1) buffer atoms_out
//{
    //Atom atoms[];
//} Out;

float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}


void next(){
    In.atoms[i].v += In.atoms[i].a;
    In.atoms[i].pos += In.atoms[i].v;
    In.atoms[i].pos.w=1.0;
}


void limits(){
    //limits
    if (In.atoms[i].pos.x > 1000){
        In.atoms[i].pos.x == 1000;
        In.atoms[i].v.x = - In.atoms[i].v.x ;
    }

    if (In.atoms[i].pos.y > 1000){
        In.atoms[i].pos.y == 1000;
        In.atoms[i].v.y = - In.atoms[i].v.y ;
    }

    if (In.atoms[i].pos.z > 1000){
        In.atoms[i].pos.z = 1000;
        In.atoms[i].v.z = - In.atoms[i].v.z ;
    }

        if (In.atoms[i].pos.x < 0){
        In.atoms[i].pos.x = 0;
        In.atoms[i].v.x = - In.atoms[i].v.x ;
    }

    if (In.atoms[i].pos.y < 0){
        In.atoms[i].pos.y = 0;
        In.atoms[i].v.y = - In.atoms[i].v.y ;
    }

    if (In.atoms[i].pos.z < 0){
        In.atoms[i].pos.z = 0;
        In.atoms[i].v.z = - In.atoms[i].v.z ;
    }
}

void main()
{
    Atom atom_i, atom_j;
    atom_i = In.atoms[i];
    //In.atoms[i].pos.x +=rand(atom_i.pos.yz);
    
    next();
    limits();

    float sum = 0;
    float r, a;
    vec3 delta;
    for (int j=0;j<In.atoms.length();j++){
        if (i == j) continue;
        //atom_j = In.atoms[i];
        delta = In.atoms[i].pos.xyz - In.atoms[j].pos.xyz;
        //delta = atom_i.pos.xyz - atom_j.pos.xyz;
        r = distance(atom_i.pos.xyz, atom_j.pos.xyz );
        a = -1/r*0.01;
    }

    Out.atoms[i].a.xyz = delta/r*a;
    Out.atoms[i].a.w = 0;
    //Out.atoms[i].a.xyz = vec3(0.001,0.001,0.001);
}