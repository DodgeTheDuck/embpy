 Light:Position,Color,Linear,Quadratic,: viewPos:vec3: : #version 330 core
out vec4 FragColor;

layout (location = 0) out vec3 attPosition;
layout (location = 1) out vec3 attNormal;
layout (location = 2) out vec4 attAlbedoSpec;
layout (location = 3) out vec4 attMetallicRoughness;
layout (location = 4) out vec4 attDepth;

struct Light {
    vec3 Position;
    vec3 Color;
    float Linear;
    float Quadratic;
};
const int NR_LIGHTS = 1;
uniform vec3 viewPos;

void main()
{                 
    vec3 diffuse = 
}   #version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 3) in vec2 aTexCoords;

out vec2 TexCoords;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0); 
    TexCoords = aTexCoords;
}