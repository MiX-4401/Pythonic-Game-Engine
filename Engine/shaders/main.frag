// Main Engine Fragment Shader 

# version 460 core


//Set uniforms
uniform sampler2D sourceTexture; 

// Set ins-outs
in vec2 uvs;
out vec4 fragColour;


// Main vertex function
//
void main(){
    vec4 sourceImage = texture(sourceTexture, uvs).rgba;
    
    fragColour = vec4(sourceImage.rgb, sourceImage.a);
}