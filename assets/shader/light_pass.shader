  #version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1,1,1,1);
} p:v:m: #version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{
    gl_Position = p * v * m * vec4(aPos, 1.0);
}