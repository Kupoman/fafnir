#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;

out VertexData {
    vec4 barycoord;
};

void main()
{
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
