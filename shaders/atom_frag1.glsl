#version 330 core
out vec4 color;
in vec3 ObjectColor;
in vec3 Normal;
in vec3 FragPos;

void main()
{
    vec3 lightPos = vec3(1.0f,1.0f,1.0f);
    vec3 lightColor = vec3(1.0f,1.0f,1.0f);
    //vec3 norm = normalize(Normal);
    float ambientStrength = 0.5f;
    vec3 ambient = ambientStrength * lightColor;
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(Normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    vec3 result = (diffuse + ambient) * ObjectColor;
    color = vec4(result, 1.0f);
}