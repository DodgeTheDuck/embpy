#version 330
out vec4 FragColor;

in vec3 frag_pos;
in vec3 frag_norm;
in vec2 frag_uv;
in vec3 frag_diffuse;

uniform sampler2D tex;
uniform int has_texture;

void main()
{

    vec3 lightPos = vec3(-1,1,-1);
    vec3 norm = normalize(frag_norm);
    vec3 lightDir = normalize(lightPos - frag_pos);    

    float light_level = max(dot(norm, lightDir), 1.0);    

    if(has_texture == 1) {
        FragColor = texture(tex, frag_uv) * light_level;
    } else {
        FragColor = vec4(frag_diffuse * light_level, 1);
    }
        
}