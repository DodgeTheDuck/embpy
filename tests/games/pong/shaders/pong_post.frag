#version 420 core
out vec4 frag_color;
  
in vec2 tex_coords;

layout(binding = 0) uniform sampler2D input_albedo;
layout(binding = 1) uniform sampler2D input_depth;

float 		width;
float 		height;
float       far;
float       near;

mat3 sobel_x = mat3( 
    1.0, 2.0, 1.0, 
    0.0, 0.0, 0.0, 
   -1.0, -2.0, -1.0 
);
mat3 sobel_y = mat3( 
    1.0, 0.0, -1.0, 
    2.0, 0.0, -2.0, 
    1.0, 0.0, -1.0 
);

float LinearizeDepth(float z)
{
     float n = near;
     float f = far;
     return (2.0 * n) / (f + n - z * (f - n));  
}

void main()
{

    near = 0.1;
    far = 1000.0;

    vec3 diffuse = texture(input_albedo, tex_coords.xy).rgb;
    mat3 I;
    vec3 texel;    
    for (int i=0; i<3; i++) {
        for (int j=0; j<3; j++) {
            vec3 depth = texelFetch(input_depth, ivec2(gl_FragCoord) + ivec2(i-1, j-1), 0).rgb;            
            vec3 tempvec = vec3(LinearizeDepth(depth.x)); 
            I[i][j] = length(tempvec);
        }
    }

    float gx = dot(sobel_x[0], I[0]) + dot(sobel_x[1], I[1]) + dot(sobel_x[2], I[2]); 
    float gy = dot(sobel_y[0], I[0]) + dot(sobel_y[1], I[1]) + dot(sobel_y[2], I[2]);

    float g = sqrt(pow(gx, 2.0)+pow(gy, 2.0));
    
    if(g < 0.1) {
        discard;
    }

    frag_color = vec4(1, 1, 1, 1);

}