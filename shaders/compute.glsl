#version 430

// Set up our compute groups
layout(local_size_x=55, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
// Some examples:
//uniform vec2 screen_size;
uniform int nframes;
uniform int gravity;
uniform int redox;

//uniform float frame_time;
float BONDR = 4.0;
uniform float BOND_KOEFF;
uniform float ATTRACT_KOEFF;
uniform float INTERACT_KOEFF;
uniform float ROTA_KOEFF;
float REPULSION1 = -3;
uniform float REPULSION_KOEFF1;
float REPULSION2 = 6;
uniform float REPULSION_KOEFF2;



// Structure of the ball data
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
        if (q1+q2==0) { q1=0; q2=0; return 1;}
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
    //if (nframes>30) return; 
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
        if (r==0) continue;
        if (r<(sumradius+REPULSION1))
           a = 1/r*  REPULSION_KOEFF1;
        else if (r<(sumradius+REPULSION2))
            a = 1/r* REPULSION_KOEFF2;

            //float qi=0, qj=0;
            //for (int ni = 0; ni<atom_i.ncount; ni++ ) qi+=atom_i.nodes[ni].pos.w;
            //for (int nj = 0; nj<atom_j.ncount; nj++ ) qj+=atom_j.nodes[nj].pos.w;
            //if(r>sumradius+REPULSION2)
                //a+= qi*qj*INTERACT_KOEFF/r;

            //a += -0.0005;
        E += delta/r*a;   //
        //random redox 
        if (redox==1){
            if (pos_i.x<100){
                if (rand(v_i.xy)>=0.9997) {atom_i.nodes[0].q = -1;
                //atom_i.color = vec4(1,0,0,1)    ;
                }
            }
            if (pos_i.x>900)
                if (rand(v_i.xy+1)>=0.9997) atom_i.nodes[0].q = 1;
        }
        
        //
        if (r<100) {
             float rn;
             vec3 nE,ni_realpos,nj_realpos,ndelta;
             vec3 allnE = vec3(0,0,0);  
             for (int ni = 0; ni<atom_i.ncount; ni++ ) {
                ni_realpos = rotate_vector(atom_i.nodes[ni].pos.xyz, atom_i.rot);
                float q1=atom_i.nodes[ni].q;
                nE = vec3(0.0,0.0,0.0);
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    nj_realpos = rotate_vector(atom_j.nodes[nj].pos.xyz, atom_j.rot);
                    ndelta =  ni_realpos - nj_realpos + delta;
                    rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    //r2n = ndelta.x*ndelta
                    float q2=atom_j.nodes[nj].q;
                    //if (rn == 0) continue;
                    a = 0;
                    //bonds update 
                    
                    if (rn<=BONDR && In.atoms[i].nodes[ni].bonded==0 && In.atoms[j].nodes[nj].bonded==0 ){
                        int canbond = shift_q(atom_i.type, atom_j.type, q1,q2);
                        if (canbond==1){
                            atom_i.nodes[ni].q=q1;
                            atom_i.nodes[ni].bonded=1;
                            if (atom_i.nodes[ni].bonded==0.0) atom_i.color = vec4(0,1,0,1);
                            atom_i.nodes[ni].pair=(j+1)*(nj+1);
                        }
                    }                            

                    //if (rn>BONDR && rn<BONDR+3 && In.atoms[i].nodes[ni].bonded==1 && In.atoms[j].nodes[nj].bonded==1){
                    if (rn>BONDR && In.atoms[i].nodes[ni].bonded==1 && In.atoms[j].nodes[nj].bonded==1 && In.atoms[i].nodes[ni].pair == (j+1)*(nj+1) && In.atoms[j].nodes[nj].pair == (i+1)*(ni+1)){
                        atom_i.nodes[ni].bonded=0;
                        atom_i.nodes[ni].pair=-1;
                    }                            
                    
                    //node interact
                    //if (rn<=BONDR && In.atoms[i].nodes[ni].bonded==1 && In.atoms[j].nodes[nj].bonded==1){
                    if (rn<=BONDR && In.atoms[i].nodes[ni].bonded==1 && In.atoms[j].nodes[nj].bonded==1 && In.atoms[i].nodes[ni].pair == (j+1)*(nj+1) && In.atoms[j].nodes[nj].pair == (i+1)*(ni+1) ){
                            a = -rn*BOND_KOEFF;
                            if (In.atoms[i].nodes[ni].q + In.atoms[j].nodes[nj].q !=0){
                                atom_i.nodes[ni].bonded=0;
                                atom_i.nodes[ni].pair=-1;
                            }
                    }
                    if ( rn>BONDR && In.atoms[i].nodes[ni].bonded==0 && In.atoms[j].nodes[nj].bonded==0 && nframes>2){
                            if (rn!=0) a= q1*q2*INTERACT_KOEFF/rn;
                    }

                            vec3 target_direction = nj_realpos + pos_j - pos_i;
                            vec3 v1 = normalize(ni_realpos);
                            vec3 v2 = normalize(target_direction);
                            float dt = dot(v1,v2);
                            if(dt>1) dt=1;
                            if(dt<-1) dt=-1;
                            if (v1!=v2){
                                    vec3 axis = cross(v1,v2);
                                    float angle = acos(dt);
                                    angle = -angle* a * ROTA_KOEFF;
                                    vec4 rot = vec4(sin(angle/2.0)* axis,cos(angle/2.0) ); // quat
                                    totalrot = normalize(qmul(rot, totalrot));
                            }


                    if (rn!=0) nE += ndelta/rn*a;
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
        v_i = normalize(v_i);
    }

//dumping
    v_i *=0.9999;      
//next
    v_i += E/(atom_i.m);
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