#version 330
#extension GL_ARB_enhanced_layouts : require

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

uniform int material_index;

in vec4 p3d_Vertex;
in vec3 p3d_Normal;

layout(xfb_buffer=0, xfb_stride=32) out;
out VertexData {
    vec4 barycoord;
    layout(xfb_offset=0) vec4 vertex;
    layout(xfb_offset=16) vec3 normal;
};

void main()
{
    vertex = p3d_ModelViewMatrix * p3d_Vertex;
    vertex.w = material_index;
    normal = normalize(p3d_NormalMatrix * p3d_Normal);
    barycoord = vec4(0.5, 1.0, 0.0, 1.0);
    gl_Position = p3d_ProjectionMatrix * vertex;
}
