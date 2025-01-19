#version 430 
out vec4 color;
in vec4 ObjectColor;
in vec3 Normal;
in vec3 FragPos;

uniform vec3 lightPos;
uniform int transparency;

void main()
{
//    color = vec4(1,1,1,1);

    vec3 lightPos2 = vec3(1.0f,1.0f,1.0f);
    
    if (transparency==2){
        if (ObjectColor.w==1.0) discard;
    }
    if (transparency==1){
        if (ObjectColor.w<1.0) discard;
    }

    vec3 lightColor = vec3(1.0f,1.0f,1.0f);
    float ambientStrength = 0.5f;
    vec3 ambient = ambientStrength * lightColor;
    vec3 lightDir = normalize(lightPos2 - FragPos);
    float diff = max(dot(Normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    vec3 result = (diffuse + ambient) * ObjectColor.xyz;
    color = vec4(result, ObjectColor.w);
}