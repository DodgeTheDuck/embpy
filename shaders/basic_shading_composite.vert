
#version 330 core
layout (location = 0) in vec3 a_pos;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{
    gl_Position = p * v * m * vec4(a_pos, 1.0);
}  