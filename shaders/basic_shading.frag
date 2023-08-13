#version 420 core
out vec4 frag_color;

in vec3 frag_pos;
in vec2 tex_coords;
in vec3 normal;
in mat3 tbn;
in vec3 eye_pos;

layout(binding = 0) uniform sampler2D albedo;
layout(binding = 2) uniform sampler2D normal_map;

struct Light {
    vec3 position;
    vec3 color;
    float intensity;
    float attenuation;
};

uniform Light lights[8];  // Up to 8 lights

uniform vec3 cameraPosition;
const float shininess = 32.0;

void main()
{
    // Sample the normal map and transform the normal
    vec3 sampledNormal = texture(normal_map, tex_coords).rgb * 2.0 - 1.0;
    vec3 transformedNormal = normalize(tbn * sampledNormal);

    // Lighting calculations
    vec3 viewDir = normalize(eye_pos - frag_pos);
    vec3 normalDir = normalize(transformedNormal);

    vec3 totalDiffuse = vec3(0.0);
    vec3 totalSpecular = vec3(0.0);

    for (int i = 0; i < 8; ++i)
    {
        if(lights[i].intensity == 0) continue;
        vec3 lightDir = normalize(lights[i].position - frag_pos);
        vec3 halfDir = normalize(lightDir + viewDir);

        float diffuseFactor = max(dot(normalDir, lightDir), 0.0);
        float specularFactor = pow(max(dot(normalDir, halfDir), 0.0), shininess);

        vec3 diffuse = lights[i].color * (diffuseFactor * lights[i].intensity);
        vec3 specular = lights[i].color * (specularFactor * lights[i].intensity);

        // Attenuation calculation
        float distance = length(lights[i].position - frag_pos);
        float attenuation = 1.0 / (1.0 + lights[i].attenuation * distance * distance);

        totalDiffuse += attenuation * diffuse;
        totalSpecular += attenuation * specular;
    }

    vec3 finalColor = totalDiffuse + totalSpecular;

    // Combine lighting with texture color
    vec3 albedoColor = texture(albedo, tex_coords).rgb;
    frag_color = vec4(albedoColor * finalColor, 1.0);
}