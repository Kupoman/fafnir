#version 420

uniform int material_index;
uniform int window_width;

in VertexData {
    vec4 barycoord;
    flat int primid;
};

out vec4 out_data;

void main()
{
    /*uint intersection_index = uint(gl_FragCoord.y)*window_width + uint(gl_FragCoord.x);*/

    out_data.rg = barycoord.xy;
    out_data.b = primid;
    out_data.a = material_index + 1.0;

    /*
    out_data[0].r = uintBitsToFloat(packUnorm2x16(barycoord.xy));
    out_data[0].g = intBitsToFloat(primid);

    out_data[1].r = intBitsToFloat(material_index);
    out_data[1].g = uintBitsToFloat(intersection_index);
    */
}
