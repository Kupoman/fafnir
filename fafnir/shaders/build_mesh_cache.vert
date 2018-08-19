#version 330
#extension GL_ARB_enhanced_layouts : require

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

uniform int material_index;

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;

layout(xfb_buffer=0, xfb_stride=64) out;
out VertexData {
    layout(xfb_offset=0) vec4 vertex;
    layout(xfb_offset=16) vec3 normal;
    layout(xfb_offset=32) vec2 texcoord0;
};

void main()
{
    vertex = p3d_ModelViewMatrix * p3d_Vertex;
    vertex.w = material_index;
    normal = normalize(p3d_NormalMatrix * p3d_Normal);
    texcoord0 = p3d_MultiTexCoord0;
    gl_Position = p3d_ProjectionMatrix * vertex;
}
