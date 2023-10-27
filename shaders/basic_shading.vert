#version 420
layout (location = 0) in vec3 a_pos;
layout (location = 1) in vec3 a_normal;
layout (location = 2) in vec3 a_tangent;
layout (location = 3) in vec2 a_tex_coords;

out vec3 frag_pos;
out vec2 tex_coords;
out vec3 normal;
out mat3 tbn;
out vec3 eye_pos;
out vec4 shadow_coord;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;
uniform mat4 depth_biased_mvp;

void main()
{
    vec4 world_pos = m * vec4(a_pos, 1.0);
    frag_pos = world_pos.xyz;
    tex_coords = a_tex_coords;

    vec3 T = normalize(vec3(m * vec4(a_tangent,   0.0)));
    vec3 N = normalize(vec3(m * vec4(a_normal,    0.0)));
    vec3 B = normalize(vec3(m * vec4(cross(N, T), 0.0)));

    normal = N;
    tbn = mat3(T, B, N);

    mat4 inverse_view = inverse(v);
    eye_pos = vec3(inverse_view[3][0], inverse_view[3][1], inverse_view[3][2]);

    gl_Position = p * v * world_pos;
    shadow_coord = depth_biased_mvp * world_pos;
}
