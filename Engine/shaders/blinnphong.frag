// BlinnPhong Lighting Fragment Shader

# version 460 core

// Set structures
struct Light {
    vec3 pos;
    vec4 colour;
    vec3 fallOff;
};

struct AmbientLight {
    vec4 colour;
};

// Set uniforms
uniform sampler2d tScene;
uniform sampler2d tNormal;
uniform vec2 resolution;
uniform int numLights;

// Set ins-outs
in vec2 uvs;
out vec4 fragColour;

// Set Uniform blocks
layout (std140) uniform LightBlock {
    Light lights[numLights];
};

layout (std140) uniform AmbientLightBlock {
    AmbientLight ambient;
}

void main(){
    // Get texture/normal maps 
    vec4 iAlbedo = texture(tScene, uvs).rgba;
    vec3 iNormal = texture(tNormal, uvs).rgb;
    vec3 normal  = normalize(iNormal * 2.0 - 1.0);

    // Get ambient light
    vec3  ambientColour    = ambient.rgb;
    float ambientIntensity = ambient.a;
    vec3 finalColour = ambientColour * ambientIntensity;

    // Per-light Blinn-Phong lighting loop
    //
    for (int i=0; i<numLights; i++) {
        // Extract light variables
        Light lightSource     = lights[i];
        vec3  lightColour     = lightSource.colour.rgb;
        float lightIntensity  = lightSource.colour.a;
        vec3  lightPos        = lightSource.pos;
        vec3  lightFallOff    = lightSource.fallOff;

        lightColour = lightColour * lightIntensity;

        // Blinn-Phong Calculations
        vec3  lightDir = vec3(lightPos.xy - (gl_FragCoord.xy / resolution.xy), lightPos.z);
        vec3  lightRay = normalize(lightDir);
        float lightDistance = length(lightDir);

        // Define fragmnet colour
        vec3 diffuseColour = lightColour * max(dot(normal, lightRay), 0.0);
        float attentuation = 1.0 / (lightFallOff.x + (lightFallOff.y * lightDistance) + (lightFallOff.z * lightDistance * lightDistance));
        finalColour += diffuseColour * attentuation;
    }

    fragColour = vec4(ialbedo.rgb * finalColour, iAlbedo.a);
}