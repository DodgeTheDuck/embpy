  scaMetallic:float: :scaRoughness:float: :texAlbedo:sampler2D: :texNormal:sampler2D: :texMetallicRoughness:sampler2D: : #version 330 core

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
}  p:mat4: :v:mat4: :m:mat4: : #version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec3 aTang;
layout (location = 3) in vec2 aTexCoords;

out vec3 FragPos;
out vec2 TexCoords;
out vec3 Normal;
out mat3 TBN;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{
    vec4 worldPos = m * vec4(aPos, 1.0);
    FragPos = worldPos.xyz;
    TexCoords = aTexCoords;    

    vec3 T = normalize(vec3(m * vec4(aTang,   0.0)));
    vec3 N = normalize(vec3(m * vec4(aNormal,    0.0)));
    vec3 B = normalize(vec3(m * vec4(cross(N, T), 0.0)));

    TBN = mat3(T, B, N);

    gl_Position = p * v * worldPos;
}