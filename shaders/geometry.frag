#version 330 core

layout (location = 0) out vec3 attPosition;
layout (location = 1) out vec3 attNormal;
layout (location = 2) out vec4 attAlbedoSpec;
layout (location = 3) out vec4 attMetallicRoughness;

in vec2 TexCoords;
in vec3 FragPos;
in vec3 Normal;
in mat3 TBN;

uniform float scaMetallic;
uniform float scaRoughness;

uniform sampler2D texAlbedo;
uniform sampler2D texNormal;
uniform sampler2D texMetallicRoughness;

void main()
{    
    attPosition = FragPos;    

    vec3 normal = texture(texNormal, TexCoords).rgb;
    normal = normal * 2.0 - 1.0;   
    normal = normalize(TBN * normal); 

    attNormal = normal;
    attAlbedoSpec.rgb = texture(texAlbedo, TexCoords).rgb;
    attAlbedoSpec.a = texture(texAlbedo, TexCoords).a;
    attMetallicRoughness = texture(texMetallicRoughness, TexCoords);
    attMetallicRoughness.g *= scaRoughness;
    attMetallicRoughness.b *= scaMetallic;
}