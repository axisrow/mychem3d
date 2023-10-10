#version 430

// Set up our compute groups
layout(local_size_x=100, local_size_y=1) in;

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


void limits(inout vec3 pos,  inout vec3 v){
    //limits
    if (pos.x > 1000){
        pos.x = 1000;
        v.x = -v.x ;
    }

    if (pos.y > 1000){
        pos.y = 1000;
        v.y = - v.y ;
    }

    if (pos.z > 1000){
        pos.z = 1000;
        v.z = - v.z ;
    }

    if (pos.x < 0){
        pos.x = 0;
        v.x = - v.x ;
    }

    if (pos.y < 0){
        pos.y = 0;
        v.y = - v.y ;
    }

    if (pos.z < 0){
        pos.z = 0;
        v.z = v.z ;
    }
}

void main()
{
    Atom atom_i, atom_j;
    vec3 pos_i,pos_j, v_i, v_j;
    
    atom_i = In.atoms[i];
    
    pos_i= atom_i.pos.xyz;
    v_i = atom_i.v.xyz;
    //In.atoms[i].pos.x +=rand(atom_i.pos.yz);

    //next
    v_i += atom_i.a.xyz;
    v_i *=0.995;
    pos_i += v_i;
    limits(pos_i,v_i);


    float sum = 0;
    float r, a;
    vec3 delta;
    vec3 sum_a = vec3(0,0,0);
    vec3 E = vec3(0,0,0);
    for (int j=0;j<In.atoms.length();j++){
        if (i == j) continue;
        atom_j = In.atoms[j];
        pos_j = atom_j.pos.xyz;
        delta = pos_i - pos_j;
        //delta = atom_i.pos.xyz - atom_j.pos.xyz;
        r = distance(pos_i, pos_j);
        a = 0;
        if (r<10)
            a = 1/r*0.5;
        else 
            a = - 1/r*0.01;
        
        E += delta/r*a;
    }
    
    Atom atom_out=atom_i;

    atom_out.a.xyz = E;
    //atom_out.a.xyz = vec3(0.01,0.01,0.01);
    atom_out.v.xyz = v_i;
    atom_out.pos.xyz = pos_i;
    Out.atoms[i] = atom_out;
}