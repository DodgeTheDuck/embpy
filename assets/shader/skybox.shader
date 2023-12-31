  skybox:samplerCube: : #version 330 core
out vec4 frag_color;

in vec3 tex_coords;

uniform samplerCube skybox;

void main()
{    
    frag_color = texture(skybox, tex_coords);
}  p:mat4: :v:mat4: : #version 330 core
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