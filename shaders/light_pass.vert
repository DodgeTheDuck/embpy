#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 3) in vec2 aTexCoords;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

out vec2 TexCoords;

void main()
{

    TexCoords = aTexCoords;
    gl_Position = p * v * m * vec4(aPos, 1.0);
}