 texAlbedo:texMetallicRoughness:texNormal:scaMetallic:scaRoughness:hasTexture:viewPos:blinn: #version 330 core
out vec4 FragColor;

in VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec3 LightPos;
    mat3 TBN;
} fs_in;


uniform sampler2D texAlbedo;
uniform sampler2D texMetallicRoughness;
uniform sampler2D texNormal;

uniform float scaMetallic;
uniform float scaRoughness;

uniform int hasTexture;
uniform vec3 viewPos;
uniform bool blinn;

const float PI = 3.14159265359;
// ----------------------------------------------------------------------------
float DistributionGGX(vec3 N, vec3 H, float roughness)
{
    float a = roughness*roughness;
    float a2 = a*a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH*NdotH;

    float nom   = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;

    return nom / denom;
}

// ----------------------------------------------------------------------------
float GeometrySchlickGGX(float NdotV, float roughness)
{
    float r = (roughness + 1.0);
    float k = (r*r) / 8.0;

    float nom   = NdotV;
    float denom = NdotV * (1.0 - k) + k;

    return nom / denom;
}
// ----------------------------------------------------------------------------
float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness)
{
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2 = GeometrySchlickGGX(NdotV, roughness);
    float ggx1 = GeometrySchlickGGX(NdotL, roughness);

    return ggx1 * ggx2;
}
// ----------------------------------------------------------------------------
vec3 fresnelSchlick(float cosTheta, vec3 F0)
{
    return F0 + (vec3(1.0) - F0) * pow(1.0 - cosTheta, 5.0);
}
// ----------------------------------------------------------------------------
void main()
{           
    
    vec3 normalMapSample = texture(texNormal, fs_in.TexCoords).rgb;
    vec3 N = normalize(normalMapSample * 2.0 - 1.0);    
    N = normalize(fs_in.TBN * N);

    vec3 V = normalize(viewPos - fs_in.FragPos);
    
    vec3 lightPos = fs_in.LightPos;
    vec3 lightColor = vec3(3000, 3000, 3000);
    vec3 albedo;
    if(hasTexture == 1) {
        albedo = texture(texAlbedo, fs_in.TexCoords).rgb;
    } else {
        albedo = vec3(1.0, 1.0, 1.0); //fs_in.Albedo;
    }

    vec4 metalRough = texture(texMetallicRoughness, fs_in.TexCoords);
    float metallic = metalRough.b * scaMetallic;
    float roughness = metalRough.g * scaRoughness;
    float ao = metalRough.r;

    vec3 F0 = vec3(0.04);
    F0 = mix(F0, albedo, metallic);

    vec3 L = normalize(lightPos - fs_in.FragPos);
    vec3 H = normalize(V + L);
    float distance = length(lightPos - fs_in.FragPos);
    float attenuation = 1.0 / (distance * distance);    
    vec3 radiance = lightColor * attenuation;

    // Cook-Torrance BRDF
    float NDF = DistributionGGX(N, H, roughness);   
    float G   = GeometrySmith(N, V, L, roughness);      
    vec3 F    = fresnelSchlick(clamp(dot(H, V), 0.0, 1.0), F0);
        
    vec3 numerator    = NDF * G * F; 
    float denominator = max(dot(N, V), 0.001); // + 0.0001 to prevent divide by zero
    vec3 specular = numerator / denominator;
    
    // kS is equal to Fresnel
    vec3 kS = F;
    // for energy conservation, the diffuse and specular light can't
    // be above 1.0 (unless the surface emits light); to preserve this
    // relationship the diffuse component (kD) should equal 1.0 - kS.
    vec3 kD = vec3(1.0) - kS;
    // multiply kD by the inverse metalness such that only non-metals 
    // have diffuse lighting, or a linear blend if partly metal (pure metals
    // have no diffuse light).
    kD *= 1.0 - metallic;	  

    // scale light by NdotL
    float NdotL = max(dot(N, L), 0.0);        

    // add to outgoing radiance Lo
    vec3 Lo = (kD * albedo / PI + specular) * radiance * NdotL;

    // ambient
    vec3 ambient = vec3(0.03) * albedo * ao;
    vec3 color = ambient + Lo;

    // HDR tonemapping
    color = color / (color + vec3(1.0));
    // gamma correct
    color = pow(color, vec3(1.0/2.0)); 

    //FragColor = vec4(color, 1.0);
    FragColor = vec4(color, 1.0);

} p:v:m: #version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec3 aTang;
layout (location = 3) in vec2 aTexCoords;

// declare an interface block; see 'Advanced GLSL' for what these are.
out VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec3 LightPos;
    mat3 TBN;
} vs_out;

uniform mat4 p;
uniform mat4 v;
uniform mat4 m;

void main()
{

    vec3 T = normalize(vec3(m * vec4(aTang, 0.0)));
    vec3 N = normalize(vec3(m * vec4(aNormal, 0.0)));    
    T = normalize(T - dot(T, N) * N);    
    vec3 B = cross(N, T);

    vs_out.FragPos = (m * vec4(aPos, 1.0)).xyz;
    vs_out.LightPos = vec3(0, 80, -40);
    vs_out.Normal = N;
    vs_out.TBN = mat3(T, B, N);
    vs_out.TexCoords = aTexCoords;
    gl_Position = p * v * m * vec4(aPos, 1.0);
}