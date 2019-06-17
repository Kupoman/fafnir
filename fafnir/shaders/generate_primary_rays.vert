#version 330

const vec2 quad_vertices[4] = vec2[4](
    vec2( -1.0, -1.0),
    vec2( 1.0, -1.0),
    vec2( -1.0, 1.0),
    vec2( 1.0, 1.0)
);

uniform mat4 p3d_ViewProjectionMatrixInverse;

out vec3 origin;
out vec3 direction;

void main()
{
    vec2 vertex = quad_vertices[gl_VertexID];

    vec4 far_plane = p3d_ViewProjectionMatrixInverse * vec4(vertex, 1.0, 1.0);
    far_plane /= far_plane.w;

    vec4 near_plane = p3d_ViewProjectionMatrixInverse * vec4(vertex, -1.0, 1.0);
    near_plane /= near_plane.w;

    direction = far_plane.xyz - near_plane.xyz;
    origin = near_plane.xyz;
    gl_Position = vec4(vertex, 0.0, 1.0);
}
