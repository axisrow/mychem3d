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
uniform int softbox;

//uniform float frame_time;
float BONDR = 4;
uniform float BOND_KOEFF;
uniform float ATTRACT_KOEFF;
uniform float INTERACT_KOEFF;
uniform float INTERACT_KOEFF2=1.0;
uniform float ROTA_KOEFF;
float REPULSION1 = -3;
uniform float REPULSION_KOEFF1;
float REPULSION2 = 10;
uniform float REPULSION_KOEFF2;
uniform float MASS_KOEFF;
uniform float NEARDIST;
uniform float HEAT;
float WIDTH = box.x;
float HEIGHT = box.y;
float DEPTH = box.z;


//float etable[11]=float[](5,500,1,4,400,6,600,3,2,200,100);
//(5,1,4,6,3,2);
float ktab[6][6] = {  {0.5, 1.5, 1.0, 1.0, 0.1, 1.0},
                      {1.5, 0.5, 1.0, 1.5, 2.0, 1.0},
                      {1.0, 1.0, 1.0, 1.0, 0.1, 1.0},
                      {1.0, 1.5, 1.0, 1.5, 0.1, 1.0},
                      {0.1, 2.0, 0.1, 0.1, 1.0, 0.1},
                      {1.0, 1.0, 1.0, 1.0, 0.1, 1.0} };

float getk(float t1 , float t2){
    if (t1>=100.0) t1 /=100.0 ;
    if (t2>=100.0) t2 /=100.0 ;
    return ktab[int(t1-1.0)][int(t2-1.0)];
}


// Structure of the ball data
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

    if (softbox==1) {
        if (pos.x > WIDTH){
            v.x -= 0.005*(pos.x - WIDTH) ;
        }

        if (pos.y > HEIGHT){
            v.y -= 0.005 *(pos.y - HEIGHT);
        }

        if (pos.z > DEPTH){
            v.z -= 0.005 * (pos.z - DEPTH);
        }

        if (pos.x < 0){
            v.x += 0.005 * (0 - pos.x );
        }

        if (pos.y < 0){
            v.y += 0.005 * (0 - pos.y );
        }

        if (pos.z < 0){
            v.z += 0.005 * (0 - pos.z );
        }
    }
    else {
            if (pos.x > WIDTH-radius){
                pos.x = WIDTH-radius;
                v.x = -v.x ;
            }   

            if (pos.y > HEIGHT-radius){
                pos.y = HEIGHT-radius;
                v.y = - v.y ;
            }

            if (pos.z > DEPTH-radius){
                pos.z = DEPTH-radius;
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
}


int shift_q(in float type1, in float type2, inout float q1, inout float q2){
    float etable[11]=float[](5,500,1,4,400,6,600,3,2,200,100);
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
    if (stage==1){  //calc q and rpos of nodes
       In.atoms[i].q=0;
       for (int ni = 0; ni<In.atoms[i].ncount; ni++ ) {
                In.atoms[i].nodes[ni].rpos.xyz = rotate_vector(In.atoms[i].nodes[ni].pos.xyz, In.atoms[i].rot);
                In.atoms[i].q+= In.atoms[i].nodes[ni].q;
       } 
       return;
    }

    Atom atom_i;
    vec3 pos_i,pos_j, v_i, v_j;
    float r;   //distance between atoms
    vec3 delta;  //coordinates delta
    float f1,f2,f3;
    vec3 F;
    atom_i = In.atoms[i];
    pos_i= atom_i.pos.xyz;

    if (stage==2){ //calc near atoms  and far field
        int index = 0;
        F = vec3(0,0,0);
        for (int j=0;j<In.atoms.length();j++){
            if (i == j) continue;
            r = distance(pos_i, In.atoms[j].pos.xyz);
            if (r==0) continue;
            if (r<NEARDIST){
                Near.indexes[i][index+1]=j;
                index++;
            }
            else {  //far field
                delta = In.atoms[i].pos.xyz - In.atoms[j].pos.xyz;
                f1= In.atoms[i].q*In.atoms[j].q*INTERACT_KOEFF/r;
                F += f1 * delta/r;  
            }

        }
        Near.indexes[i][0]=index;  // near atoms count
        Far.F.xyz = F;
        return;
    }

    if(stage==3){   //autospinset
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = atom_i.nodes[ni].rpos.xyz;
            if (atom_i.nodes[ni].spin ==0){
                for (int j=0;j<i;j++){  //half matrix
                    Atom atom_j = In.atoms[j];
                    pos_j = atom_j.pos.xyz;
                    delta = pos_i - pos_j;
                    r =     distance(pos_i, pos_j);
                    if (r==0) continue;
                    for (int nj = 0; nj<atom_j.ncount; nj++){
                        vec3 nj_realpos = atom_j.nodes[nj].rpos.xyz;
                        vec3 ndelta =  ni_realpos - nj_realpos + delta;
                        float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                        if (rn<BONDR){
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
            }
        }                
        return;
    }

    if (stage==4){
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = atom_i.nodes[ni].rpos.xyz;
            float bonded = 0.0;
            for (int jj=1;jj<=Near.indexes[i][0];jj++){
                int j = Near.indexes[i][jj];
                Atom atom_j = In.atoms[j];
                pos_j = atom_j.pos.xyz;
                delta = pos_i - pos_j;
                r =     distance(pos_i, pos_j);
//                if (r==0) continue;
                if (r>=40) continue;
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    vec3 nj_realpos = atom_j.nodes[nj].rpos.xyz;
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
                    atom_i.animate = 500;                    
                }
            }
            if (pos_i.x>WIDTH-300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = -1;
                    atom_i.animate = 500;
                }
            }    
    }


    for (int jj=1;jj<=Near.indexes[i][0];jj++){
        int j = Near.indexes[i][jj];
        //if (i == j) continue;
        Atom atom_j = In.atoms[j];
        pos_j = atom_j.pos.xyz;
        delta = pos_i - pos_j;
        r = distance(pos_i, pos_j);
        if (r==0) continue;

        //if (r<300){
            f1= atom_i.q*atom_j.q*INTERACT_KOEFF/r;
            F += delta/r*f1;  
        //}

        if (r<40) {
             f2 = 0;
             float sumradius = atom_i.r + atom_j.r;
             if (r<(sumradius+REPULSION1))
                f2 = 1/r*  REPULSION_KOEFF1;
             else if (r<(sumradius+REPULSION2))
                f2 = 1/r* REPULSION_KOEFF2;
             F += delta/r*f2;

             //nodes   
             float rn;
             vec3 nF,ndelta;
             vec3 allnF = vec3(0,0,0);  
             for (int ni = 0; ni<atom_i.ncount; ni++ ) {
                vec3 ni_realpos = atom_i.nodes[ni].rpos.xyz;
                float ni_q=atom_i.nodes[ni].q;
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    vec3 nj_realpos = atom_j.nodes[nj].rpos.xyz;
                    ndelta =  ni_realpos - nj_realpos + delta;
                    rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    nF = vec3(0.0,0.0,0.0);

                    //r2n = ndelta.x*ndelta
                    float nj_q=atom_j.nodes[nj].q;
                    if (rn == 0) continue;
                    f3 = 0;
                    float k = getk(atom_i.type, atom_j.type);
                    //node interact
                    //if (rn<=BONDR ){
                    if (rn<=BONDR ){                        
                        int canbond = shift_q(atom_i.type, atom_j.type, ni_q,nj_q);
                        atom_i.nodes[ni].q=ni_q;
                        if (atom_i.nodes[ni].spin !=0 && atom_i.nodes[ni].spin + atom_j.nodes[nj].spin==0 && canbond ==1){
                            f3 = -rn* BOND_KOEFF*k;
                            //v_i *=0.5;
                        }
                        else {
                            f3 = 1/rn;
                        }
                    }
                    if (rn>BONDR && rn < BONDR*2 ){
                        f3+= k* atom_i.nodes[ni].spin * atom_j.nodes[nj].spin * INTERACT_KOEFF2/rn/rn;
                    }
                    if (atom_i.nodes[ni].bonded == 0.0 && atom_j.nodes[nj].bonded==0.0 &&  atom_i.nodes[ni].spin + atom_j.nodes[nj].spin==0 ){
                        f3+= k* atom_i.nodes[ni].spin * atom_j.nodes[nj].spin * INTERACT_KOEFF2/rn/rn;
                    }

                    if (atom_i.nodes[ni].bonded == 0.0 && atom_j.nodes[nj].bonded==0.0 &&  atom_i.nodes[ni].q + atom_j.nodes[nj].q==0 &&  atom_i.nodes[ni].spin + atom_j.nodes[nj].spin==0 ){
                        f3+= atom_i.nodes[ni].q * atom_j.nodes[nj].q * INTERACT_KOEFF2/rn/rn;

                    }



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

                    nF += ndelta/rn*f3;
                    F += nF;
                }
                
            }
            //F += allnF;
        } //if r <100

    } //forj
    
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
    pos_i += v_i;
    atom_i.rot = normalize(qmul(atom_i.rotv,atom_i.rot));
    
//limits    
    limits(pos_i,v_i,atom_i.r); //borders of container
    

    atom_i.v.xyz = v_i;
    atom_i.pos.xyz = pos_i;
    Out.atoms[i] = atom_i;
}