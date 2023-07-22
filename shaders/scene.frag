#version 330 core
out vec4 FragColor;

in VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec3 Tang;
} fs_in;


uniform sampler2D albedo;
uniform sampler2D metallicRoughness;

uniform int hasTexture;
uniform vec3 viewPos;
uniform bool blinn;

void main()
{           

    vec3 lightPos = vec3(5, 5, 5);
    vec3 color;
    if(hasTexture == 1) {
        color = texture(albedo, fs_in.TexCoords).rgb;
    } else {
        color = vec3(1.0, 1.0, 1.0); //fs_in.Albedo;
    }

    vec4 metalRough = texture(metallicRoughness, fs_in.TexCoords);
    float metallic = metalRough.g;
    float roughness = metalRough.r;

    // ambient
    vec3 ambient = 0.05 * color;
    // diffuse
    vec3 lightDir = normalize(lightPos - fs_in.FragPos);
    vec3 normal = normalize(fs_in.Normal);
    float diff = max(dot(lightDir, normal), 0.0);
    vec3 diffuse = diff * color;
    // specular
    vec3 viewDir = normalize(viewPos - fs_in.FragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = 0.0;
 
    vec3 halfwayDir = normalize(lightDir + viewDir);  
    spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);    

    vec3 specular = mix(vec3(0.04), color, metallic) * spec;
    specular *= 1.0 - roughness;
    FragColor = vec4(ambient + diffuse + specular, 1.0);
}