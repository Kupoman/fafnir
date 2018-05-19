#version 330

layout(triangles) in;
layout(triangle_strip) out;
layout(max_vertices=3) out;

in VertexData {
    vec4 barycoord;
} v_in[];

out VertexData {
    vec4 barycoord;
};

void main()
{
    for (int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        barycoord = vec4(i==0, i==1, i==2, 1.0);
        EmitVertex();
    }
}
