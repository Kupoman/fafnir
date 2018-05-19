#version 330

uniform int material_index;

in VertexData {
    vec4 barycoord;
};

out vec4 out_data;

void main()
{
    out_data.rg = barycoord.xy;
    out_data.b = 0;
    out_data.a = material_index + 1.0;
}
