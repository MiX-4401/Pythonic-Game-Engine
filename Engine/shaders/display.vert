// Main Engine Vertex Shader

# version 460 core

// Set ins-outs
in vec2 aTexCoord;
in vec2 aPosition;
out vec2 uvs;

// Main Vertex function
//
void main(){
    uvs = aTexCoord;
    gl_Position = vec4(aPosition, 0.0, 1.0);
}