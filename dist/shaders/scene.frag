#version 330 core
out vec4 FragColor;

in VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec3 Tang;
} fs_in;

uniform int hasTexture;
uniform sampler2D tex;
uniform vec3 viewPos;
uniform bool blinn;

void main()
{           

    vec3 lightPos = vec3(0, 5, 0);
    vec3 color;
    if(hasTexture == 1) {
        color = texture(tex, fs_in.TexCoords).rgb;
    } else {
        color = vec3(1.0, 1.0, 1.0); //fs_in.Albedo;
    }
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

    vec3 specular = vec3(0.0) * spec; // assuming bright white light color
    FragColor = vec4(ambient + diffuse + specular, 1.0);
}