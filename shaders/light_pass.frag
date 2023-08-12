#version 330 core
out vec4 FragColor;

layout (location = 0) out vec3 attDiffuse;
layout (location = 1) out vec3 attSpecular;

uniform sampler2D texPosition;
uniform sampler2D texAlbedo;
uniform sampler2D texMetallicRoughness;
uniform sampler2D texNormal;
uniform sampler2D texDepth;

uniform vec3 viewPos;

uniform vec3 LightPos;
uniform vec3 LightColor;
uniform float LightIntensity;
uniform int LightType;
uniform vec3 LightDir;

void main()
{           
    
    vec2 texCoord = gl_FragCoord.xy / vec2(1920, 1080);

    vec3 fragPos = texture(texPosition, texCoord).rgb;
    fragPos.z = texture(texDepth, texCoord).r;

    vec3 normal = texture(texNormal, texCoord).rbg;

    float dist = length(LightPos - fragPos);
    float atten = 1.0 - clamp(dist / LightIntensity, 0.0, 1.0);

    if(atten == 0.0) {
        discard;
    }

    vec3 incident = normalize(LightPos - fragPos);
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 halfDir = normalize(incident + viewDir);

    float lambert = clamp(dot(incident, normal), 0.0, 1.0);
    float rFactor = clamp(dot(halfDir, normal), 0.0, 1.0);
    float sFactor = pow(rFactor, 33.0);

    attDiffuse = vec3(LightColor.xyz * lambert * atten);
    attSpecular = vec3(LightColor.xyz * sFactor * atten * 0.33);

    // vec3 radiance = LightColor * LightIntensity * attenuation;
    
    // // Cook-Torrance BRDF
    // float NDF = DistributionGGX(N, H, roughness);   
    // float G   = GeometrySmith(N, V, L, roughness);      
    // vec3 F    = fresnelSchlick(clamp(dot(H, V), 0.0, 1.0), F0);
        
    // vec3 numerator    = NDF * G * F; 
    // float denominator = max(dot(N, V), 0.001); // + 0.0001 to prevent divide by zero
    // vec3 specular = numerator / denominator;

    // attPosition = specular;
    // attPosition = F;
    // // kS is equal to Fresnel
    // vec3 kS = F;
    // // for energy conservation, the diffuse and specular light can't
    // // be above 1.0 (unless the surface emits light); to preserve this
    // // relationship the diffuse component (kD) should equal 1.0 - kS.
    // vec3 kD = vec3(1.0) - kS;
    // // multiply kD by the inverse metalness such that only non-metals 
    // // have diffuse lighting, or a linear blend if partly metal (pure metals
    // // have no diffuse light).
    // kD *= 1.0 - metallic;	  

    // // scale light by NdotL
    // float NdotL = max(dot(N, L), 0.0);

    // // add to outgoing radiance Lo
    // vec3 Lo = (kD * albedo / PI + specular) * radiance * NdotL;

    // attNormal = vec3(0.03) * albedo * ao;

    // // // ambient
    // //  = vec3(0.03) * albedo * ao;
    // // vec3 color = ambient + Lo;

    // // // HDR tonemapping
    // // color = color / (color + vec3(1.0));
    // // // gamma correct
    // // color = pow(color, vec3(1.0/2.0)); 
    
    // // FragColor = vec4(color, 1.0);

}