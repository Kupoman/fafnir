#version 330

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

in vec4 p3d_Vertex;
in vec3 p3d_Normal;

out VertexData {
    vec4 barycoord;
    vec4 vertex;
    vec3 normal;
};

void main()
{
    vertex = p3d_ModelViewMatrix * p3d_Vertex;
    normal = normalize(p3d_NormalMatrix * p3d_Normal);
    barycoord = vec4(0.5, 1.0, 0.0, 1.0);
    gl_Position = p3d_ProjectionMatrix * vertex;
}
