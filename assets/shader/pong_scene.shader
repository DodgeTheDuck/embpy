  albedo_col:vec3: : #version 420 core

uniform vec3 albedo_col;

in vec2 tex_coords;

out vec4 frag_color;

void main()
{
    frag_color = vec4(albedo_col, 1.0);
}  p:mat4: :v:mat4: :m:mat4: : #version 420
layout (location = 0) in vec3 a_pos;
layout (location = 3) in vec2 a_tex_coords;

out vec3 frag_pos;
out vec2 tex_coords;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{
    gl_Position = p * v * m * vec4(a_pos, 1.0);
}
