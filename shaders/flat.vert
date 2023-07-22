#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNorm;
layout (location = 2) in vec4 aTang;
layout (location = 3) in vec2 aTexCoord_0;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

out vec3 norm;
out vec2 texCoord_0;

void main()
{
    norm = aNorm;
    texCoord_0 = aTexCoord_0;
    gl_Position = p * v * m * vec4(aPos, 1.0);
}