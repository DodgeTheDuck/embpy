#version 330 core
layout (location = 0) in vec3 a_pos;
layout (location = 3) in vec2 a_tex_coords;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

out vec2 tex_coords;

void main()
{

    tex_coords = a_tex_coords;
    gl_Position = p * v * m * vec4(a_pos, 1.0);
}