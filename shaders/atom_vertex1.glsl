#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform vec3 objectColor;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 Normal;
out vec3 ObjectColor;
out vec3 FragPos;  


void main()
{ 
    gl_Position = projection * view * model * vec4(position, 1.0f);
    ObjectColor = objectColor;
    FragPos = vec3(model * vec4(position, 1.0f));
    Normal = normal;
}