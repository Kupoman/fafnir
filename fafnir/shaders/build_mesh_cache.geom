#version 330
#extension GL_ARB_enhanced_layouts : require

layout(triangles) in;
layout(triangle_strip) out;
layout(max_vertices=3) out;

uniform int primitive_offset;

in VertexData {
    vec4 barycoord;
    vec4 vertex;
    vec3 normal;
} v_in[];

layout(xfb_buffer=0, xfb_stride=16) out;
out VertexData {
    vec4 barycoord;
    layout(xfb_offset=0) vec4 vertex;
};

void main()
{
    for (int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        gl_PrimitiveID = primitive_offset + gl_PrimitiveIDIn;
        barycoord = vec4(i==0, i==1, i==2, 1.0);
        vertex = v_in[i].vertex;
        EmitVertex();
    }
}
