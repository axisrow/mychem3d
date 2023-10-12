#version 430

// Set up our compute groups
layout(local_size_x=50, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
// Some examples:
//uniform vec2 screen_size;
uniform int gravity;
//uniform float frame_time;
float BONDR = 4;
float BOND_KOEFF = 0.2;
float ATTRACT_KOEFF= 0.5;
float ROTA_KOEFF = 0.000001;
float REPULSION1 = -3;
float REPULSION_KOEFF1 = 15;
float REPULSION2 = 5;
float REPULSION_KOEFF2= 1.5;



// Structure of the ball data
struct Node {
    vec4 pos;
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
    vec4 color;
    Node nodes[5];
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

void limits(inout vec3 pos,  inout vec3 v, in float radius){
    if(v.x>1) v.x=1;
    if(v.y>1) v.y=1;
    if(v.z>1) v.z=1;
    if(v.x<-1) v.x=-1;
    if(v.y<-1) v.y=-1;
    if(v.z<-1) v.z=-1;

    if (pos.x > 1000-radius){
        pos.x = 1000-radius;
        v.x = -v.x ;
    }

    if (pos.y > 1000-radius){
        pos.y = 1000-radius;
        v.y = - v.y ;
    }

    if (pos.z > 1000-radius){
        pos.z = 1000-radius;
        v.z = - v.z ;
    }

    if (pos.x < radius){
        pos.x = radius;
        v.x = - v.x ;
    }

    if (pos.y < radius){
        pos.y = radius;
        v.y = - v.y ;
    }

    if (pos.z < radius){
        pos.z = radius;
        v.z = -v.z ;
    }
}


int shift_q(in float type1, in float type2, inout float q1, inout float q2){
    float etable[7]=float[](5,1,4,400,6,3,2);
    int i1,i2;
    for(int i=0;i<etable.length();i++){
        if (etable[i]==type1){
            i1 = i;
            break;
        }
    }
    for(int i=0;i<etable.length();i++){
        if (etable[i]==type2){
            i2 = i;
            break;
        }
    }
    if (i1>i2){
        if (q1== 0 && q2== 0 ){ q1=-1; q2= 1; return 1;}  //1
        if (q1== 0 && q2==-1 ){ q1=-1; q2= 0; return 0;}  //2
        if (q1== 0 && q2== 1 ){ q1= 0; q2= 1; return 0;}  //3
        if (q1==-1 && q2== 0 ){ q1=-1; q2= 0; return 0;}
        if (q1==-1 && q2==-1 ){ q1=-1; q2=-1; return 0;}
        if (q1==-1 && q2== 1 ){ q1=-1; q2= 1; return 1;}
        if (q1== 1 && q2== 0 ){ q1= 0; q2= 1; return 0;}
        if (q1== 1 && q2==-1 ){ q1=-1; q2= 1; return 1;}   //8
        if (q1== 1 && q2== 1 ){ q1= 1; q2= 1; return 0;}   //9
    }
    if (i1==i2){
        if (q1+q2==0) return 1;
        else return 0;
    }
    if (i1<i2){
        if (q1== 0 && q2== 0 ){ q1= 1; q2=-1; return 1;}  //1
        if (q1== 0 && q2==-1 ){ q1= 0; q2=-1; return 0;}  //2
        if (q1== 0 && q2== 1 ){ q1= 1; q2= 0; return 0;}  //3
        if (q1==-1 && q2== 0 ){ q1= 0; q2=-1; return 0;}
        if (q1==-1 && q2==-1 ){ q1=-1; q2=-1; return 0;}
        if (q1==-1 && q2== 1 ){ q1= 1; q2=-1; return 1;}
        if (q1== 1 && q2== 0 ){ q1= 1; q2= 0; return 0;}
        if (q1== 1 && q2==-1 ){ q1= 1; q2=-1; return 1;}   //8
        if (q1== 1 && q2== 1 ){ q1= 1; q2= 1; return 0;}   //9
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



    float sum = 0;
    float r;   //distance between atoms
    float a;   //acceleration
    float sumradius;   
    vec3 delta;  //coordinates delta
    vec3 sum_a = vec3(0.0,0.0,0.0);
    vec3 E = vec3(0.0,0.0,0.0);
    vec4 totalrot = vec4(0.0, 0.0, 0.0, 1.0);
    
    for (int j=0;j<In.atoms.length();j++){
        if (i == j) continue;
        atom_j = In.atoms[j];
        pos_j = atom_j.pos.xyz;
        delta = pos_i - pos_j;
        sumradius = atom_i.r + atom_j.r;
        r = distance(pos_i, pos_j);
        a = 0;
        if (r!=0){
            if (r<(sumradius+REPULSION1))
                a = 1/r * REPULSION_KOEFF1;
            if (r<(sumradius+REPULSION2))
                a = 1/r * REPULSION_KOEFF2;

            //a += -0.0005;
            E += delta/r*a;   //
        }
        float rn;
        vec3 nE,ni_realpos,nj_realpos,ndelta;
        vec3 allnE = vec3(0,0,0);  
        if (r<100) {
            for (int ni = 0; ni<atom_i.ncount; ni++ ) {
                nE = vec3(0.0,0.0,0.0);
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    ni_realpos = rotate_vector(atom_i.nodes[ni].pos.xyz, atom_i.rot);
                    nj_realpos = rotate_vector(atom_j.nodes[nj].pos.xyz, atom_j.rot);
                    ndelta =  ni_realpos - nj_realpos + delta;
                    rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    //r2n = ndelta.x*ndelta
                    if (rn == 0) continue;
                    a = 0;
                    float q1 = atom_i.nodes[ni].pos.w;
                    float q2 =  atom_j.nodes[nj].pos.w;
                    if (rn<BONDR){
                        int bonded = shift_q(atom_i.type, atom_j.type, q1,q2);
                        atom_i.nodes[ni].pos.w=q1;
                        if (bonded==1)
                            a = -rn*rn*BOND_KOEFF;
                    }
                    else {
                      a = q1*q2*0.1;
                    }
                    nE += ndelta/rn*a;

                    vec3 target_direction = nj_realpos + pos_j - pos_i;
                    vec3 v1 = normalize(ni_realpos);
                    vec3 v2 = normalize(target_direction);
                    float dt = dot(v1,v2);
                    if(dt>1) dt=1;
                    if(dt<-1) dt=-1;
                    if (v1!=v2){
                        vec3 axis = cross(v1,v2);
                        float angle = acos(dt);
                        angle = angle * ROTA_KOEFF *100;
                        vec4 rot = vec4(sin(angle/2)* axis,cos(angle/2) ); // quat
                        totalrot = normalize(qmul(rot, totalrot));
                    }

                }
                allnE += nE;
            }

            E += allnE;
        }
    }
    
    //totalrot = vec4(0, sin(-0.01),sin(-0.01), cos(-0.01));    
    //atom_i.rotv = normalize(qmul(totalrot, atom_i.rotv));
    atom_i.rotv = totalrot;

 // mixer
    if (atom_i.type==100){
        //if( dot(v_i, v_i) < 0.8) v_i*2;
        if (v_i.x>0) v_i.x=1;
        if (v_i.y>0) v_i.y=1;
        if (v_i.z>0) v_i.z=1;
        if (v_i.x<0) v_i.x=-1;
        if (v_i.y<0) v_i.y=-1;
        if (v_i.z<0) v_i.z=-1;
        //v_i += a*0.01;
    }

//dumping
    v_i *=0.9999;      
//next
    v_i += E/atom_i.m;;
    if (gravity==1) v_i.y -= 0.001; //gravity
    pos_i += v_i;
    atom_i.rot = normalize(qmul(atom_i.rotv,atom_i.rot));
    
//limits    
    limits(pos_i,v_i,atom_i.r); //borders of container
    

    //atom_out.a.xyz = vec3(0.01,0.01,0.01);
    atom_i.v.xyz = v_i;
    atom_i.pos.xyz = pos_i;
    Out.atoms[i] = atom_i;
}