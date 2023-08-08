#version 330 core
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