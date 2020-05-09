#version 330

const vec2 quad_vertices[4] = vec2[4]( vec2( -1.0, -1.0), vec2( 1.0, -1.0), vec2( -1.0, 1.0), vec2( 1.0, 1.0));

uniform int instance_id;

void main()
{
    gl_Position = vec4(quad_vertices[gl_VertexID], instance_id / 16777215.0, 1.0);
}
