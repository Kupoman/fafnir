#version 330

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

uniform samplerBuffer buffer_meshes;

out VertexData {
    vec4 barycoord;
    flat float material_index;
};

void main()
{
    int vertexStride = 2;
    int vertexIdBase = int(gl_VertexID * vertexStride);
    vec4 data = texelFetch(buffer_meshes, vertexIdBase + 0);
    vec4 vertex = vec4(data.xyz, 1.0);

    int vertexNumber = gl_VertexID % 3;
    barycoord = vec4(vertexNumber == 0, vertexNumber == 1, vertexNumber == 2, 1.0);
    material_index = data.w;
    gl_Position = p3d_ProjectionMatrix * vertex;
}
