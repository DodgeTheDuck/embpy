#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aAlbedo;

// declare an interface block; see 'Advanced GLSL' for what these are.
out VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec3 Albedo;
} vs_out;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{
    vs_out.FragPos = (m * vec4(aPos, 1.0)).xyz;
    vs_out.Normal = aNormal;
    vs_out.TexCoords = aTexCoords;
    vs_out.Albedo = aAlbedo;
    gl_Position = p * v * m * vec4(aPos, 1.0);
}