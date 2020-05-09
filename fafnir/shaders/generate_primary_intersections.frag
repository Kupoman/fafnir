#version 330

in VertexData {
    vec4 barycoord;
    flat float material_index;
    flat float object_id;
};

out vec4 out_data;

void main()
{
    out_data.rg = barycoord.xy;
    out_data.b = gl_PrimitiveID;
    out_data.a = object_id;
}
