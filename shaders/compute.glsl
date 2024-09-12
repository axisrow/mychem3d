#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
// Some examples:
//uniform vec2 screen_size;
uniform int stage;
uniform vec3 box;
uniform int iTime;
uniform int bondlock;
uniform int gravity;
uniform int redox;
uniform int shake;

//uniform float frame_time;
float BONDR = 4;
uniform float BOND_KOEFF;
uniform float ATTRACT_KOEFF;
uniform float INTERACT_KOEFF;
uniform float INTERACT_KOEFF2=1.0;
uniform float ROTA_KOEFF;
float REPULSION1 = -6;
uniform float REPULSION_KOEFF1;
uniform float REPULSION_KOEFF2;
uniform float MASS_KOEFF;
uniform float NEARDIST;
uniform float HEAT;
float WIDTH = box.x;
float HEIGHT = box.y;
float DEPTH = box.z;


//(5,1,4,6,3,2);
float ktab[6][6] = {  {0.5, 1.5, 1.0, 1.0, 0.1, 1.0},
                      {1.5, 0.5, 1.0, 1.5, 2.0, 1.0},
                      {1.0, 1.0, 1.0, 1.0, 0.1, 1.0},
                      {1.0, 1.5, 1.0, 1.5, 0.1, 1.0},
                      {0.1, 2.0, 0.1, 0.1, 1.0, 0.1},
                      {1.0, 1.0, 1.0, 1.0, 0.1, 1.0} };

float tbl_elneg[18]= float[] (0, 2.2, 0.0, 0.0, 0.0,
                                0.0, 2.55, 3.04, 3.44,
                                0.0,  0.0,  0.93, 0.0,
                                0.0,  0.0,  2.19, 2.58, 3.16);

//float tbl_ncount

float getk(float t1 , float t2){
    return ktab[int(t1-1.0)][int(t2-1.0)];
}


// Structure of the ball data
struct Node {
    vec4 pos;
    float q;
    float bonded;
    float type;
    float spin;
};

struct Atom
{
    vec4 pos;
    vec4 v;
    float type;
    float r;
    float m;
    float ncount;
    vec4 rot;
    vec4 rotv;
    float animate;
    float q;
    float fxd;
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

layout(std430, binding=2) buffer near_atoms
{
    int indexes[][NEARATOMSMAX];
} Near;

layout(std430, binding=3) buffer far_field
{
    vec4 F;
} Far;

layout(std430, binding=4) buffer rpos_buffer
{
    vec4 rpos[][6];
};

layout(std430, binding=5) buffer q_buffer
{
    float qbuffer[];
};

layout(std430, binding=6) buffer qs_buffer
{
    float qshift_buffer[][6];
};



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
    v = clamp(v , vec3(-MAXVEL,-MAXVEL,-MAXVEL), vec3(MAXVEL,MAXVEL,MAXVEL));

    vec3 outlim;
    outlim = pos - box;
    outlim = clamp(outlim,vec3(0.0),vec3(100.0));
    v -= outlim * 0.005;
    outlim = clamp(pos, vec3(-100.0), vec3(0.0));
    v -= outlim * 0.005;
}



bool shift_q(in float type1, in float type2, inout float q1, inout float q2, inout float s1, inout float s2){
    float etable[6]=float[](5,1,4,6,3,2);
    int i1,i2;
    for(int i=0;i<etable.length();i++){
        if (etable[i]==type1){
            i1 = i;
            //break;
        }
    }
    for(int i=0;i<etable.length();i++){
        if (etable[i]==type2){
            i2 = i;
            //break;
        }
    }
    if (i1>i2){
        if (q1== 0 && q2== 0 ){ q1=-1; q2= 1; return true;}  //1  shift 1
        if (q1== 0 && q2==-1 ){ q1=-1; q2= 0; s2=-s1; return false;}  //2  shift 1
        if (q1== 0 && q2== 1 ){ q1= 0; q2= 1; return false;}  //3
        if (q1==-1 && q2== 0 ){ q1=-1; q2= 0; return false;}
        if (q1==-1 && q2==-1 ){ q1=-1; q2=-1; return false;}
        if (q1==-1 && q2== 1 ){ q1=-1; q2= 1; return true;}
        if (q1== 1 && q2== 0 ){ q1= 0; q2= 1; s1=s2; return false;} //shift 1
        if (q1== 1 && q2==-1 ){ q1=-1; q2= 1; return true;}   //8  shift 2
        if (q1== 1 && q2== 1 ){ q1= 1; q2= 1; return false;}   //9
    }
    if (i1==i2){
        if (q1+q2==0) { q1=0; q2=0; return true;}
        else return false;
    }
    if (i1<i2){
        if (q1== 0 && q2== 0 ){ q1= 1; q2=-1; return true;}  //1 shift
        if (q1== 0 && q2==-1 ){ q1= 0; q2=-1; return false;}  //2
        if (q1== 0 && q2== 1 ){ q1= 1; q2= 0; s2=s1; return false;}  //3 shift
        if (q1==-1 && q2== 0 ){ q1= 0; q2=-1; s1=-s2; return false;}  // shift
        if (q1==-1 && q2==-1 ){ q1=-1; q2=-1; return false;}
        if (q1==-1 && q2== 1 ){ q1= 1; q2=-1; return true;}   //shift
        if (q1== 1 && q2== 0 ){ q1= 1; q2= 0; return false;} 
        if (q1== 1 && q2==-1 ){ q1= 1; q2=-1; return true;}   //8
        if (q1== 1 && q2== 1 ){ q1= 1; q2= 1; return false;}   //9
    }
}



void main()
{
    if (stage==1){  //calc q and rpos of nodes
       //In.atoms[i].q=0;
       float q = 0; 
       for (int ni = 0; ni<In.atoms[i].ncount; ni++ ) {
                rpos[i][ni].xyz = rotate_vector(In.atoms[i].nodes[ni].pos.xyz, In.atoms[i].rot);
                q += qshift_buffer[i][ni] + In.atoms[i].nodes[ni].q;
                qshift_buffer[i][ni] = 0;
                
       } 
       In.atoms[i].q = q;
       return;
    }

    Atom atom_i;
    vec3 pos_i,v_i;
    //float r;   //distance between atoms
    //vec3 delta,delta2;  //coordinates delta
    //float f1,f2;
    vec3 F;
    atom_i = In.atoms[i];
    pos_i= atom_i.pos.xyz;

    if (stage==2){ //calc near atoms  and far field
        int index = 0;
        F = vec3(0,0,0);
        for (int j=0;j<In.atoms.length();j++){
            if (i == j) continue;
            float r = distance(pos_i, In.atoms[j].pos.xyz);
            if (r==0) continue;
            if (r<NEARDIST){
                Near.indexes[i][index+1]=j;
                index++;
            }
            else {  //far field
                vec3 delta = In.atoms[i].pos.xyz - In.atoms[j].pos.xyz;
                float f1= In.atoms[i].q*In.atoms[j].q*INTERACT_KOEFF/r;
                F += f1 * delta/r;  
            }

        }
        Near.indexes[i][0]=index;  // near atoms count
        Far.F.xyz = F;
        return;
    }

    if(stage==3){   //auto spin set
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = rpos[i][ni].xyz;
            float ni_type = atom_i.nodes[ni].type;
            if (ni_type>1) continue;
            if (atom_i.nodes[ni].spin ==0){
                for (int j=0;j<i;j++){  //half matrix
                    Atom atom_j = In.atoms[j];
                    vec3 pos_j = atom_j.pos.xyz;
                    vec3 delta = pos_i - pos_j;
                    float r =     distance(pos_i, pos_j);
                    if (r==0) continue;
                    for (int nj = 0; nj<atom_j.ncount; nj++){
                        vec3 nj_realpos = rpos[j][nj].xyz;
                        float nj_type = atom_j.nodes[nj].type;
                        if (nj_type>1) continue;
                        /*if (ni_type==1){
                            float rn = distance(pos_i , pos_j + nj_realpos);
                            vec3 ndelta =  pos_i - (pos_j + nj_realpos);
                            if (rn==0) continue;
                            ni_realpos = -ndelta/rn * atom_i.r;
                        }
                        if (nj_type==1){
                            float rn = distance(pos_i + ni_realpos, pos_j);
                            vec3 ndelta =  (pos_i + ni_realpos)-pos_j ;
                            if (rn==0.0) continue;
                            nj_realpos = ndelta/rn * atom_j.r;
                        } */                       
                        vec3 ndelta =  ni_realpos - nj_realpos + delta;
                        float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                        if (rn<BONDR){
                            In.atoms[i].nodes[ni].bonded=1.0;
                            if (atom_j.nodes[nj].spin !=0){
                                In.atoms[i].nodes[ni].spin = - atom_j.nodes[nj].spin;
                            }
                            else {
                                In.atoms[i].nodes[ni].spin = 1;
                                In.atoms[j].nodes[nj].spin = -1;
                            }
                        }
                    }
                }
                if (In.atoms[i].nodes[ni].spin==0) In.atoms[i].nodes[ni].spin=1;
            }
        }                
        return;
    }

    if (stage==4){ // bonded state set
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = rpos[i][ni].xyz;
            float ni_type = atom_i.nodes[ni].type;
            float bonded = 0.0;
            if (ni_type>1) continue;
            for (int jj=1;jj<=Near.indexes[i][0];jj++){
                int j = Near.indexes[i][jj];
                Atom atom_j = In.atoms[j];
                vec3 pos_j = atom_j.pos.xyz;
                vec3 delta = pos_i - pos_j;
                float r =     distance(pos_i, pos_j);
                //if (r>=40) continue;
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    float nj_type = atom_j.nodes[nj].type;
                    vec3 nj_realpos = rpos[j][nj].xyz;
                    if (nj_type>1) continue;
                    vec3 ndelta =  ni_realpos - nj_realpos + delta;
                    float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    
                    if (rn<=BONDR){
                        bonded = 1.0;
                    }
                }
            }
            In.atoms[i].nodes[ni].bonded = bonded;
            //In.atoms[i].color = vec4(1.0);
        }
        return;
    }

    v_i = atom_i.v.xyz;
    //In.atoms[i].pos.x +=rand(atom_i.pos.yz);

    F = vec3(0.0,0.0,0.0);
    vec4 totalrot = vec4(0.0, 0.0, 0.0, 1.0);

    
//  animate
    if (atom_i.animate >0) atom_i.animate-=1;

    //random redox 
    if (redox==1){
            if (pos_i.x<300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = 1;
                    atom_i.nodes[0].spin = 1;
                    atom_i.animate = 500;                    
                }
            }
            if (pos_i.x>WIDTH-300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = -1;
                    atom_i.nodes[0].spin = -1;
                    atom_i.animate = 500;
                }
            }    
    }

    float bondcheck[5]= {0.0,0.0,0.0,0.0,0.0};


    for (int jj=1;jj<=Near.indexes[i][0];jj++){
            int j = Near.indexes[i][jj];
            Atom atom_j = In.atoms[j];
            vec3 pos_j = atom_j.pos.xyz;
            vec3 delta = pos_i - pos_j;
            float r = distance(pos_i, pos_j);
            if (r==0) continue;

            float f1= atom_i.q*atom_j.q*INTERACT_KOEFF/r;
            F += delta/r*f1;  

            float f2 = REPULSION_KOEFF2/r/r/r;
            F += delta/r*f2;

            if (r<40) {
                float f2 = 0;
                float sumradius = atom_i.r + atom_j.r;
                f2 = float(r<(sumradius+REPULSION1)) * (1/r*  REPULSION_KOEFF1) ;
                F += delta/r*f2;

            //nodes
            for (int ni = 0; ni<atom_i.ncount; ni++ ) {
                vec3 ni_realpos = rpos[i][ni].xyz;
                float ni_q=atom_i.nodes[ni].q ;
                float ni_spin = atom_i.nodes[ni].spin;
                float ni_bonded = atom_i.nodes[ni].bonded;
                float ni_type = atom_i.nodes[ni].type;

                for (int nj = 0; nj<atom_j.ncount; nj++){
                    float nj_type = atom_j.nodes[nj].type;
                    vec3 nj_realpos = rpos[j][nj].xyz;
                    float f3 = 0;
                    //node interact
                    if (ni_type!=2.0 && nj_type!=2.0){
                        /*if (ni_type==1){
                            float rn = distance(pos_i , pos_j + nj_realpos);
                            vec3 ndelta =  pos_i - (pos_j + nj_realpos);
                            if (rn==0) continue;
                            ni_realpos = -ndelta/rn * atom_i.r;
                        }

                        if (nj_type==1){
                            float rn = distance(pos_i + ni_realpos, pos_j);
                            vec3 ndelta =  (pos_i + ni_realpos)-pos_j ;
                            if (rn==0.0) continue;
                            nj_realpos = ndelta/rn * atom_j.r;
                        }*/

                        float rn;
                        vec3 ndelta;
                        /*if (atom_i.type==1){
                            //float rn_2 = distance(pos_i , pos_j + nj_realpos);
                            vec3 ndelta_2 =  pos_i - (pos_j + nj_realpos);
                            //if (rn==0) continue;
                            vec3 ni_realpos_2 = - normalize(ndelta_2) * atom_i.r;
                            ndelta =  ni_realpos_2 - nj_realpos + delta;
                            rn = distance(pos_i + ni_realpos_2, pos_j + nj_realpos);
                        }
                        else {*/
                            ndelta =  ni_realpos - nj_realpos + delta;
                            rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                        //} 

                        float nj_q=atom_j.nodes[nj].q;
                        float nj_spin=atom_j.nodes[nj].spin;
                        if (rn == 0) continue;
                        float q = tbl_elneg[int(atom_j.type)] - tbl_elneg[int(atom_i.type)];
                        
                        if (rn<=BONDR  ){                        
                            //bool canbond = shift_q(atom_i.type, atom_j.type, ni_q,nj_q, ni_spin, nj_spin);
                            //atom_i.nodes[ni].spin = ni_spin;
                            if (ni_spin + nj_spin==0 && ni_q + nj_q == 0){
                                qshift_buffer[i][ni]=0.3*q + 0.1*(atom_j.q-atom_i.q);
                                atom_i.nodes[ni].q = 0;
                                atom_i.nodes[ni].bonded=1.0;
                                bondcheck[ni]=1.0;
                                f3 = -rn* BOND_KOEFF;
                                //v_i *=0.5;
                            }
                            else {
                                f3 = 2.0;
                            }
                        }
                        
                        float nj_bonded = atom_j.nodes[nj].bonded;
                        if (rn>BONDR && rn < BONDR*1.5  ){
                            
                            f3+= abs(q) * ni_spin * nj_spin * INTERACT_KOEFF2/rn/rn;
                        }
                        
                        if (ni_bonded == 0.0 && nj_bonded ==0.0 &&  ni_spin + nj_spin==0 ){
                            f3+= abs(q) * ni_spin * nj_spin * INTERACT_KOEFF2/rn/rn;
                        }
                
                        if (ni_bonded == 0.0 && nj_bonded==0.0 && ni_q + nj_q==0 &&  ni_spin + nj_spin ==0 ){
                            f3+= ni_q * nj_q * INTERACT_KOEFF2/rn/rn;
                        }
                        
                        F += ndelta/rn*f3;
                    }




/*
                    else if(ni_type==2.0 && nj_type==1.0){
                        float rn = distance(pos_i + ni_realpos, pos_j);
                        vec3 ndelta =  (pos_i + ni_realpos)-pos_j ;
                        if (rn==0.0) continue;
                        nj_realpos = ndelta/rn * atom_j.r;
                        ndelta =  ni_realpos - nj_realpos + delta;
                        rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                        if (rn==0.0) continue;
                        if (rn<BONDR*1.0){
                        //f3 = - rn * BOND_KOEFF*0.1 ;
                            f3 = - rn * BOND_KOEFF *0.1;
                            F += ndelta/rn*f3;
                        }
                    } 
*/
                    /*else if(ni_type==1.0 && nj_type==2.0){
                        
                        float rn = distance(pos_i , pos_j + nj_realpos);
                        vec3 ndelta =  pos_i - (pos_j + nj_realpos);
                        if (rn==0) continue;

                        ni_realpos = -ndelta/rn * atom_i.r;
                        rn = distance(pos_i + ni_realpos , pos_j + nj_realpos);
                        float nj_q=atom_j.nodes[nj].q;
                        ndelta =  ( pos_i + ni_realpos) - (pos_j + nj_realpos);
                        if (rn==0) continue;
                        if (rn<BONDR*1.0){
                            //atom_i.color.xyz=vec3(1.0,0.0,0.0);    
                            f3 = - rn * BOND_KOEFF * 0.1 ;
                            F += ndelta/rn*f3;
                        }
                    }*/

                    //if(nj==0){
//
                    //}

                    vec3 target_direction = nj_realpos + pos_j - pos_i;
                    vec3 v1 = normalize(ni_realpos);
                    vec3 v2 = normalize(target_direction);
                    if (v1!=v2){
                            float dt = dot(v1,v2);
                            dt = clamp(dt,-1,1);
                            vec3 axis = cross(v1,v2);
                            float angle = acos(dt);
                            angle = -angle * f3 * ROTA_KOEFF/ (atom_i.m);
                            vec4 rot = normalize(vec4(sin(angle/2.0)* axis,cos(angle/2.0) )); // quat
                            totalrot = qmul(rot, totalrot);
                    }
                } //nj 
                
             } //if r <40

        } //for jj

    } //for ni

    for (int ni = 0; ni<atom_i.ncount; ni++ ) {
        atom_i.nodes[ni].bonded = bondcheck[ni];
    }


    //totalrot = vec4(0, sin(-0.01),sin(-0.01), cos(-0.01));    
    //atom_i.rotv = normalize(qmul(totalrot, atom_i.rotv));
    atom_i.rotv = totalrot;


 // mixer
    if (atom_i.type==100){
        if (v_i!= vec3(0.0,0.0,0.0))
            v_i = normalize(v_i);
    }

//heating
   v_i +=  v_i * HEAT*0.0001;      
   
 
 //gravity
   if (gravity==1) v_i.y -= 0.0001; //gravity

   //if (pos_i.y < 30) v_i.y += 0.1;
     
//shake
   if (shake==1) v_i+= vec3(rand(pos_i.xy)-0.5,rand(pos_i.xz)-0.5,rand(pos_i.yz)-0.5)*0.03;

// far field
   //F += Far.F.xyz*0.01;

//next
    v_i += F/(atom_i.m*MASS_KOEFF);
    if (atom_i.fxd==1)  v_i = vec3(0.0);
    pos_i += v_i;

    atom_i.rot = normalize(qmul(atom_i.rotv,atom_i.rot));
    
//limits    
    limits(pos_i,v_i,atom_i.r); //borders of container
    

    atom_i.v.xyz = v_i;
    atom_i.pos.xyz = pos_i;
    Out.atoms[i] = atom_i;
}