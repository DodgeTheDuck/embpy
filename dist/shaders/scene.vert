#version 330
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 uv;
layout (location = 3) in vec3 diffuse;

uniform mat4 m;
uniform mat4 v;
uniform mat4 p;

out vec3 frag_pos;
out vec3 frag_norm;
out vec2 frag_uv;
out vec3 frag_diffuse;

void main() {
    gl_Position = p * v * m * vec4(position, 1.0);
    frag_pos = vec3(m * vec4(position, 1.0));
    frag_norm = normal;
    frag_uv = uv;
    frag_diffuse = diffuse;
}