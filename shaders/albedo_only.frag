#version 420 core
out vec4 frag_color;

in vec2 tex_coords;

layout(binding = 0) uniform sampler2D albedo;

uniform vec3 albedo_col;

void main()
{
    frag_color = texture(albedo, tex_coords);
}