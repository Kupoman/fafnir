#version 330

uniform sampler2D texture_intersections;

out vec4 frag_color;

void main()
{
    ivec2 texel_pos = ivec2(gl_FragCoord.xy);
    vec4 data = texelFetch(texture_intersections, texel_pos, 0);
    frag_color = vec4(0.5, 1.0, 0.0, 1.0);
    gl_FragDepth = data.a / 16777215.0;
}
