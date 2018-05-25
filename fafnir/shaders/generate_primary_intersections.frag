#version 330

uniform int material_index;

in VertexData {
    vec4 barycoord;
    vec4 vertex;
    vec3 normal;
};

out vec4 out_data;

void main()
{
    out_data.rg = barycoord.xy;
    out_data.b = gl_PrimitiveID;
    out_data.a = material_index + 1.0;
}
