 albedo:normal_map:albedo_col:has_tangents:lights

uniform vec3 cameraPosition: #version 420 core
out vec4 frag_color;

in vec3 frag_pos;
in vec2 tex_coords;
in vec3 normal;
in mat3 tbn;
in vec3 eye_pos;

layout(binding = 0) uniform sampler2D albedo;
layout(binding = 2) uniform sampler2D normal_map;

uniform vec3 albedo_col;

uniform bool has_tangents;

struct Light {
    vec3 position;
    vec3 color;
    float intensity;
    float attenuation;
};

uniform Light lights[8];  // Up to 8 lights

uniform vec3 cameraPosition;
const float shininess = 32.0;

void main()
{

    vec3 ambient_color = vec3(1.0, 1.0, 1.0);
    float ambient_intensity = 0.2;

    vec3 N = vec3(0.0, 0.0, 0.0);

    if(has_tangents) {
        vec3 sampledNormal = texture(normal_map, tex_coords).rgb * 2.0 - 1.0;
        N = normalize(tbn * sampledNormal);
    } else {
        N = normal;
    }

    // Lighting calculations
    vec3 viewDir = normalize(eye_pos - frag_pos);
    vec3 normalDir = normalize(N);

    vec3 totalDiffuse = vec3(0.0);
    vec3 totalSpecular = vec3(0.0);

    for (int i = 0; i < 8; ++i)
    {
        if(lights[i].intensity == 0) continue;
        vec3 lightDir = normalize(lights[i].position - frag_pos);
        vec3 halfDir = normalize(lightDir + viewDir);

        float diffuseFactor = max(dot(normalDir, lightDir), 0.0);
        float specularFactor = pow(max(dot(normalDir, halfDir), 0.0), shininess);

        vec3 diffuse = lights[i].color * (diffuseFactor * lights[i].intensity);
        vec3 specular = lights[i].color * (specularFactor * lights[i].intensity);

        // Attenuation calculation
        float distance = length(lights[i].position - frag_pos);
        float attenuation = 1.0 / (1.0 + lights[i].attenuation * distance * distance);

        totalDiffuse += attenuation * diffuse;
        totalSpecular += attenuation * specular;
    }

    vec3 ambient = ambient_color * ambient_intensity;

    vec3 finalColor = ambient + totalDiffuse + totalSpecular;

    vec3 albedoColor = texture(albedo, tex_coords).rgb * albedo_col;
    frag_color = vec4(albedoColor * finalColor, 1.0);

} p:v:m: #version 420
layout (location = 0) in vec3 a_pos;
layout (location = 1) in vec3 a_normal;
layout (location = 2) in vec3 a_tangent;
layout (location = 3) in vec2 a_tex_coords;

out vec3 frag_pos;
out vec2 tex_coords;
out vec3 normal;
out mat3 tbn;
out vec3 eye_pos;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{
    vec4 world_pos = m * vec4(a_pos, 1.0);
    frag_pos = world_pos.xyz;
    tex_coords = a_tex_coords;
    normal = a_normal;

    vec3 T = normalize(vec3(m * vec4(a_tangent,   0.0)));
    vec3 N = normalize(vec3(m * vec4(a_normal,    0.0)));
    vec3 B = normalize(vec3(m * vec4(cross(N, T), 0.0)));

    tbn = mat3(T, B, N);

    mat4 inverse_view = inverse(v);
    eye_pos = vec3(inverse_view[3][0], inverse_view[3][1], inverse_view[3][2]);

    gl_Position = p * v * world_pos;
}
