#version 330 core
out vec4 FragColor;

in vec3 norm;
in vec2 texCoord_0;

void main()
{           
    FragColor = vec4(1.0 * norm.x, 1.0 * norm.y, 1.0 * norm.z, 1.0);
}