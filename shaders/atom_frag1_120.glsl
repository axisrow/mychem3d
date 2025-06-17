#version 120

// Varying inputs from vertex shader
varying vec4 ObjectColor;
varying vec3 Normal;
varying vec3 FragPos;

// Uniforms
uniform vec3 lightPos;
uniform int transparency;

void main()
{
    // Transparency handling
    if (transparency == 2) {
        if (ObjectColor.w == 1.0) discard;
    }
    if (transparency == 1) {
        if (ObjectColor.w < 1.0) discard;
    }

    // Basic lighting calculation
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    float ambientStrength = 0.5;
    vec3 ambient = ambientStrength * lightColor;
    
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    vec3 result = (diffuse + ambient) * ObjectColor.xyz;
    gl_FragColor = vec4(result, ObjectColor.w);
}