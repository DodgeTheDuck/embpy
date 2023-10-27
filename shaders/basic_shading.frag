#version 420 core
out vec4 frag_color;

in vec3 frag_pos;
in vec2 tex_coords;
in vec3 normal;
in mat3 tbn;
in vec3 eye_pos;
in vec4 shadow_coord;

layout(binding = 0) uniform sampler2D albedo;
layout(binding = 2) uniform sampler2D normal_map;
layout(binding = 9) uniform sampler2D shadow_map;

uniform vec3 albedo_col;
uniform bool has_tangents;

struct Light {
    vec3 position;
    vec3 color;
    float intensity;
    float attenuation;
};

uniform Light lights[8];  // Up to 8 lights

uniform vec3 cameraPosition;
const float shininess = 1.0;

void main()
{

    //frag_color = vec4(1, 0, 0, 1);
    //return;

    vec3 ambient_color = vec3(1.0, 1.0, 1.0);
    float ambient_intensity = 0.1;

    vec3 N = vec3(0.0, 0.0, 0.0);

    if(has_tangents) {      
        vec3 sampledNormal = texture(normal_map, tex_coords).rgb * 2.0 - 1.0;
        N = normalize(tbn * sampledNormal);
    } else {
        N = normal;
    }

    // Lighting calculations
    vec3 viewDir = normalize(eye_pos - frag_pos);
    vec3 normalDir = normalize(N);

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
        vec3 specular = vec3(0, 0, 0); //lights[i].color * (specularFactor * lights[i].intensity);

        // Attenuation calculation
        float distance = length(lights[i].position - frag_pos);
        float attenuation = 1.0 / (1.0 + lights[i].attenuation * distance * distance);

        totalDiffuse += attenuation * diffuse;
        totalSpecular += attenuation * specular;
    }

    vec3 ambient = ambient_color * ambient_intensity;

    vec3 finalColor = (ambient + totalDiffuse + totalSpecular);

    vec3 albedoColor = texture(albedo, tex_coords).rgb * albedo_col;
    frag_color = vec4(albedoColor * finalColor, 1.0);

}