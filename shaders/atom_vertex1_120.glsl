#version 120

// Vertex attributes (instead of layout)
attribute vec3 position;
attribute vec3 normal;

// Uniforms
uniform vec4 objectColor;
uniform int mode;
uniform int nodeindex;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Varying outputs to fragment shader
varying vec3 Normal;
varying vec4 ObjectColor;
varying vec3 FragPos;

void main()
{
    if (mode == 0) {  // VBO merge atoms and nodes 
        gl_Position = projection * view * model * vec4(position, 1.0);
        ObjectColor = objectColor;
        FragPos = vec3(model * vec4(position, 1.0));
        Normal = normal;
    }
    
    // For now, simplified mode 1 and 2 (atoms and nodes)
    // Will be handled via CPU preprocessing instead of SSBO
    if (mode == 1 || mode == 2) {
        float factor = 0.001;
        vec4 vposition = vec4(position * factor, 1.0);
        gl_Position = projection * view * vposition;
        ObjectColor = objectColor;
        FragPos = vposition.xyz;
        Normal = normal;
    }
}