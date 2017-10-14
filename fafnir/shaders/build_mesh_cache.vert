#version 420

uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex stride in texels
const int vert_stride = 2;

layout(size1x32) uniform restrict writeonly image1D buffer_vertices;

uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;
uniform int vertex_offset;


in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec4 p3d_Color;
in vec2 p3d_MultiTexCoord0;
in vec2 p3d_MultiTexCoord1;

out VertexData {
    vec4 barycoord;
    int vertexid;
};

void main()
{
    int sub_vid = gl_VertexID % 3;
    vertexid = (vertex_offset + gl_VertexID) * vert_stride;

    vec4 data;
    vec4 position = p3d_ModelViewMatrix * p3d_Vertex;
    data.xyz = position.xyz;
    data.w = packUnorm4x8(p3d_Color);
    imageStore(buffer_vertices, vertexid, data.bgra);

    vec3 normal = normalize(p3d_NormalMatrix * p3d_Normal);
    data.x = uintBitsToFloat(packSnorm2x16(normal.xy));
    data.y = uintBitsToFloat(packSnorm2x16(vec2(normal.z, 0)));
    data.z = uintBitsToFloat(packUnorm2x16(p3d_MultiTexCoord0));
    data.w = uintBitsToFloat(packUnorm2x16(p3d_MultiTexCoord1));
    imageStore(buffer_vertices, vertexid+1, data.bgra);

    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
