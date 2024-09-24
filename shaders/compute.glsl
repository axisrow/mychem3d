#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
uniform int stage;
uniform vec3 box;
uniform int iTime;
uniform int bondlock;
uniform int gravity;
uniform int redox;
uniform int shake;
uniform int highlight_unbond;
uniform int sideheat;

//uniform float frame_time;
float BONDR = 4;
uniform float BOND_KOEFF;
uniform float ATTRACT_KOEFF;
uniform float INTERACT_KOEFF;
uniform float INTERACT_KOEFF2=0.1;
uniform float ROTA_KOEFF;
uniform float CONUS_KOEFF = 0.866;
float REPULSION1 = -6;
uniform float REPULSION_KOEFF1;
uniform float REPULSION_KOEFF2;
uniform float MASS_KOEFF;
uniform float NEARDIST;
uniform float HEAT;
float WIDTH = box.x;
float HEIGHT = box.y;
float DEPTH = box.z;


float tbl_elneg[18]= float[] (0, 2.2, 0.0, 0.0, 0.0,
                                0.0, 2.55, 3.04, 3.44,
                                0.0,  0.0,  0.93, 0.0,
                                0.0,  0.0,  2.19, 2.58, 3.16);


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
    float highlight;
    float q;
    float fxd;
    float _pad;
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

layout(std430, binding=6) buffer qs_buffer
{
    float qshift_buffer[][6];
};



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
    v -= outlim * 0.005 ;
    outlim = clamp(pos, vec3(-100.0), vec3(0.0));
    v -= outlim * 0.005;
}


int i = int(gl_GlobalInvocationID);

void main()
{
    if (stage==1){  //calc atom q and rpos of nodes
       //In.atoms[i].q=0;
       float q = 0; 
       for (int ni = 0; ni<In.atoms[i].ncount; ni++ ) {
                rpos[i][ni].xyz = rotate_vector(In.atoms[i].nodes[ni].pos.xyz, In.atoms[i].rot);
                q += qshift_buffer[i][ni]; 
                if (In.atoms[i].nodes[ni].type == 2.0 ) { 
                    q +=  1;
                }
                q +=  In.atoms[i].nodes[ni].q;
                
       } 
       In.atoms[i].q = q;
       return;
    }

    vec3 F;  

    Atom atom_i = In.atoms[i];
    vec3 pos_i= atom_i.pos.xyz;

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
            //if (ni_type>1) continue;
            if (atom_i.nodes[ni].spin ==0 && atom_i.nodes[ni].q==0){
                for (int j=0;j<i;j++){  //half matrix
                    Atom atom_j = In.atoms[j];
                    vec3 pos_j = atom_j.pos.xyz;
                    vec3 delta = pos_i - pos_j;
                    float r =     distance(pos_i, pos_j);
                    if (r==0) continue;
                    for (int nj = 0; nj<atom_j.ncount; nj++){
                        vec3 nj_realpos = rpos[j][nj].xyz;
                        float nj_type = atom_j.nodes[nj].type;
                        //if (nj_type>1) continue;
                        vec3 ndelta =  ni_realpos - nj_realpos + delta;
                        float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                        if (rn<BONDR){
                            In.atoms[i].nodes[ni].bonded=1.0;
                            if (atom_j.nodes[nj].spin !=0){
                                In.atoms[i].nodes[ni].spin = - atom_j.nodes[nj].spin;
                            }
                            else {
                                //randspin
                                if (rand(atom_i.pos.xy)>=0.5){
                                    In.atoms[i].nodes[ni].spin = 1;
                                    In.atoms[j].nodes[nj].spin = -1;
                                }
                                else {
                                    In.atoms[i].nodes[ni].spin = -1;
                                    In.atoms[j].nodes[nj].spin = 1;
                                }


                            }
                        }
                    }
                }
                if (In.atoms[i].nodes[ni].spin==0) In.atoms[i].nodes[ni].spin= 2*mod(i+ni,2)-1;
            }
        }                
        return;
    }

    if (stage==4){ // bonded state set
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = rpos[i][ni].xyz;
            float ni_type = atom_i.nodes[ni].type;
            float bonded = 0.0;
            //if (ni_type>1) continue;
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
                    //if (nj_type>1) continue;
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

    vec3 v_i = atom_i.v.xyz;
    //In.atoms[i].pos.x +=rand(atom_i.pos.yz);

    F = vec3(0.0,0.0,0.0);
    vec4 totalrot = vec4(0.0, 0.0, 0.0, 1.0);

    
//  highlight
    if (atom_i.highlight >0) atom_i.highlight-=1;

    //random redox 
    if (redox==1){
            if (pos_i.x<300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = 1;
                    atom_i.nodes[0].spin = 0;
                    atom_i.highlight = 500;                    
                }
            }
            if (pos_i.x>WIDTH-300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = -1;
                    atom_i.nodes[0].spin = 0;
                    atom_i.highlight = 500;
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
            if (r<1) continue;

            float f1,f2;

            f1= atom_i.q*atom_j.q*INTERACT_KOEFF/r;
            F += delta/r*f1;  

            f2 = REPULSION_KOEFF2/r/r/r;
            F += delta/r*f2;

            if (r<60) {
                float sumradius = atom_i.r + atom_j.r;
                if (r<(sumradius+REPULSION1) ){
                   f2 =  REPULSION_KOEFF1/r ;
                   //atom_i.highlight = 50;
                }

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
                    float nj_bonded = atom_j.nodes[nj].bonded;
                    float nj_q=atom_j.nodes[nj].q;
                    float nj_spin=atom_j.nodes[nj].spin;

                    float f3 = 0;
                    //node interact
                    float rn;
                    vec3 ndelta;
                    /*
                    if (ni_type==1 && ni_bonded==0.0){
                            ni_realpos = normalize(pos_j-pos_i)*atom_i.r;
                            //ndelta =  ni_realpos - nj_realpos + delta;
                            //rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    }                        

                    if (nj_type==1 && nj_bonded==0.0){
                            nj_realpos = normalize(pos_i-pos_j)*atom_j.r;
                            //ndelta =  ni_realpos - nj_realpos + delta;
                            //rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    } */
                    
                    //if (ni_type!=2.0 && nj_type!=2.0){

                        ndelta =  ni_realpos - nj_realpos + delta;
                        rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);

                        
                        if (rn == 0) continue;
                        float edelta = tbl_elneg[int(atom_j.type)] - tbl_elneg[int(atom_i.type)];
                        
                        if (rn<=BONDR  ){                        
                            if (ni_spin + nj_spin==0 && ni_q + nj_q == 0){
                                qshift_buffer[i][ni]=0.35*edelta + 0.1*(atom_j.q-atom_i.q);
                                //if (ni_type!=2 && nj_type!=2) 
                                atom_i.nodes[ni].q = 0;
                                atom_i.nodes[ni].spin = 2*int(i<j)-1;   //+mod(time,2)?
                                bondcheck[ni]=1.0;
                                f3 = -rn* BOND_KOEFF;
                                //v_i *=0.01;
                            }
                            else {
                                f3 = 10.0/rn; // pauli!
                            }
                        }


                        
                        if (rn>BONDR && rn < BONDR*1.5  ){
                            f3+= abs(edelta) * ni_spin * nj_spin * INTERACT_KOEFF2/rn/rn;
                        }
                        
                        if (ni_bonded == 0.0 && nj_bonded ==0.0 &&  ni_spin + nj_spin==0 ){
                            f3+= ni_spin * nj_spin * INTERACT_KOEFF/rn/rn;
                        }
                                        
                        if (ni_bonded == 0.0 && nj_bonded==0.0 && ni_q + nj_q==0  ){ 
                            f3+= ni_q * nj_q * INTERACT_KOEFF/rn/rn;
                        }
                        
                        //hydrogen bond, node to atom
                        if (ni_bonded==0.0 && atom_j.type==1.0 && nj_bonded==1.0){
                                //nj_realpos = normalize(pos_i+ni_realpos-pos_j)*atom_j.r;
                                nj_realpos = vec3(0);
                                ndelta =  ni_realpos - nj_realpos + delta;
                                rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                                float conus_i  = dot(ni_realpos,-delta)/atom_i.r/length(delta);
                                if(rn>8  &&  conus_i>CONUS_KOEFF){  
                                    f3+= atom_j.q* ni_q  * INTERACT_KOEFF/rn;
                                    //atom_i.highlight = 2;                    
                                    
                                }
                        } 


                    vec3 target_direction = nj_realpos + pos_j - pos_i;
                    vec3 target_direction2 = pos_j - pos_i;
                    // nice self-align without +nj_realpos, but broke bonds, sigma&pi?
                    vec3 v1 = normalize(ni_realpos);
                    vec3 v2 = normalize(target_direction);
                    //vec3 v2 = normalize(mix(target_direction,target_direction2,0.1));
                    if (v1!=v2){
                            float dt = dot(v1,v2);
                            dt = clamp(dt,-1,1);
                            vec3 axis = cross(v1,v2);
                            float angle = acos(dt);
                            angle = -angle * f3 * ROTA_KOEFF/ (atom_i.m);
                            vec4 rot = normalize(vec4(sin(angle/2.0)* axis,cos(angle/2.0) )); // quat
                            totalrot = qmul(rot, totalrot);
                    }


                    

                    /*ndelta =  (pos_j + nj_realpos) - (pos_i + ni_realpos);
                    vec3 ndelta2 = (pos_j  + nj_realpos) - (pos_i);
                    if (f3==0) continue;
                    vec3 ff = normalize(ndelta)*f3;
                    float cf =  dot(ff,ndelta2)/abs(f3);
                    F += normalize(ndelta2)*cf;*/


                    F += ndelta/rn*f3;

                } //nj 
                
            } //for ni

            //hydrogen bond atom to node
            if (atom_i.type==1 && atom_i.nodes[0].bonded==1.0){ 
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    float nj_bonded = atom_j.nodes[nj].bonded;
                    if (nj_bonded==1.0) continue;
                    //float nj_type = atom_j.nodes[nj].type;
                    vec3 nj_realpos = rpos[j][nj].xyz;
                    float nj_q=atom_j.nodes[nj].q;
                    float nj_spin=atom_j.nodes[nj].spin;
        
                    //vec3 ni_realpos =  normalize(pos_j+nj_realpos-pos_i)*atom_i.r;
                    vec3 ni_realpos =  vec3(0);
                    vec3 ndelta =  pos_i + ni_realpos - (pos_j + nj_realpos);
                    float rn = distance(pos_i, pos_j + nj_realpos);
                    float conus_j  = dot(nj_realpos, delta)/length(delta)/atom_j.r;
                    //if (rn==0) continue;
                    if(rn> 8 && conus_j>CONUS_KOEFF){   
                                    float f3= atom_i.q* nj_q  * INTERACT_KOEFF/rn;
                                    F += ndelta/rn*f3;                                    
                                    //atom_i.highlight = 5;
                    }
                }
            }


        } //if r<40



    } //for jj



    for (int ni = 0; ni<atom_i.ncount; ni++ ) {
        float old = atom_i.nodes[ni].bonded;
        atom_i.nodes[ni].bonded = bondcheck[ni];
        if (old==1.0 && atom_i.nodes[ni].bonded==0.0) {  //unbond
            if (highlight_unbond==1) {
                atom_i.highlight = 50;                    
            }                
            if(qshift_buffer[i][ni]>0){
                atom_i.nodes[ni].q= 1;
                atom_i.nodes[ni].spin= 0;
            }
            if(qshift_buffer[i][ni]<0){
                atom_i.nodes[ni].q=-1;
                atom_i.nodes[ni].spin= 0;
            }
            qshift_buffer[i][ni] = 0;
        }


    }


    //totalrot = vec4(0, sin(-0.01),sin(-0.01), cos(-0.01));    
    //atom_i.rotv = normalize(qmul(totalrot, atom_i.rotv));
    atom_i.rotv = totalrot;


 // mixer
    if (atom_i.type==666){
        if (v_i!= vec3(0.0,0.0,0.0))
            v_i = normalize(v_i);
    }

//heating
   if (sideheat==1){
        if (pos_i.y<50.0) v_i +=  v_i * HEAT*0.0001;      
   }
   else v_i +=  v_i * HEAT*0.0001;      
   
 
 //gravity
   if (gravity==1) v_i.y -= 0.00001; //gravity

   //if (pos_i.y < 30) v_i.y += 0.1;
     
//shake
   if (shake==1) v_i+= vec3(rand(pos_i.xy)-0.5,rand(pos_i.xz)-0.5,rand(pos_i.yz)-0.5)*0.01;

// far field
   //F += Far.F.xyz*0.01;

//next
    vec3 a = F/(atom_i.m*MASS_KOEFF);
    v_i += a;
    if (atom_i.fxd==1)  v_i = vec3(0.0);
    pos_i += v_i;

    atom_i.rot = normalize(qmul(atom_i.rotv,atom_i.rot));

// 
//   if (length(v_i)>length(atom_i.v.xyz)+0.05)
//        atom_i.highlight=5;
    
//limits    
    limits(pos_i,v_i,atom_i.r); //borders of container
 
    atom_i.v.xyz = v_i;
    atom_i.pos.xyz = pos_i;
    Out.atoms[i] = atom_i;
}