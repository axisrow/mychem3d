#version 330 core
out vec4 color;
in vec3 ObjectColor;

void main()
{
    color = vec4(ObjectColor, 1.0f);
}