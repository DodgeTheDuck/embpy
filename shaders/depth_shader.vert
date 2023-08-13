
#version 330 core
layout (location = 0) in vec3 a_pos;

uniform mat4 pv;
uniform mat4 m;

void main()
{
    gl_Position = pv * m * vec4(a_pos, 1.0);
}  