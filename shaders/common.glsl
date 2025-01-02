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

