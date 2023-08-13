#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D albedo;

void main()
{           
    FragColor = texture(albedo, TexCoords);    
}