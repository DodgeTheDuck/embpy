#version 330
out vec4 FragColor;

in vec3 frag_pos;
in vec3 frag_norm;
in vec2 frag_uv;

uniform sampler2D tex;

void main()
{
    FragColor = texture(tex, frag_uv);
    // FragColor = vec4(1 * frag_uv.x, 1 * frag_uv.y, 1, 1);
}