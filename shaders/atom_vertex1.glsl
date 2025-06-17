#version 120

// Vertex attributes (GLSL 1.20 style)
attribute vec3 position;
attribute vec3 normal;

// Uniforms
uniform vec4 objectColor;
uniform int mode;
uniform int nodeindex;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Varying outputs to fragment shader (GLSL 1.20 style)
varying vec3 Normal;
varying vec4 ObjectColor;
varying vec3 FragPos;



void main()
{
    // Simplified version for OpenGL 2.1 - no SSBO support
    // Mode 0: Basic VBO rendering (default)
    if (mode == 0 || mode == 1 || mode == 2) {
        float factor = 0.001;
        gl_Position = projection * view * model * vec4(position, 1.0);
        ObjectColor = objectColor;
        FragPos = vec3(model * vec4(position, 1.0));
        Normal = normal;
    }
}