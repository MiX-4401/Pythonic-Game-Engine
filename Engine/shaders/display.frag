// Main Engine Fragment Shader 

# version 460 core


//Set uniforms
uniform sampler2D tScene; 

// Set ins-outs
in vec2 uvs;
out vec4 fragColour;


// Main vertex function
//
void main(){
    vec4 iScene = texture(tScene, uvs).rgba;
    
    fragColour = vec4(iScene.rgb, iScene.a);
}