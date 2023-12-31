  albedo:sampler2D: :albedo_col:vec3: : #version 420 core
out vec4 frag_color;

in vec2 tex_coords;

layout(binding = 0) uniform sampler2D albedo;

uniform vec3 albedo_col;

void main()
{
    frag_color = texture(albedo, tex_coords);
}  p:mat4: :v:mat4: :m:mat4: : #version 330 core
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