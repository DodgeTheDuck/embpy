#version 330 core
layout (location = 0) in vec3 a_pos;

out vec3 tex_coords;

uniform mat4 p;
uniform mat4 v;

void main()
{
    tex_coords = a_pos;
    mat3 view_no_position = mat3(v);
    vec4 pos = p * mat4(view_no_position) * vec4(a_pos, 1.0);
    gl_Position = pos.xyww;
}  