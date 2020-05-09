#version 330

uniform mat4 p3d_ViewProjectionMatrix;

uniform samplerBuffer buffer_meshes;

out VertexData {
    vec4 barycoord;
    flat float material_index;
    flat float object_id;
};

void main()
{
    int vertexStride = 4;
    int vertexIdBase = int(gl_VertexID * vertexStride);
    vec4 data = texelFetch(buffer_meshes, vertexIdBase);
    vec4 vertex = vec4(data.xyz, 1.0);
    object_id = data.w;

    int vertexNumber = gl_VertexID % 3;
    barycoord = vec4(vertexNumber == 0, vertexNumber == 1, vertexNumber == 2, 1.0);
    material_index = data.w;
    gl_Position = p3d_ViewProjectionMatrix * vertex;
}
