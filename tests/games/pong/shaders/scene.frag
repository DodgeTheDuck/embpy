#version 420 core

uniform vec3 albedo_col;

in vec2 tex_coords;

out vec4 frag_color;

void main()
{
    frag_color = vec4(albedo_col, 1.0);
}