#version 330

uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec4 p3d_Color;
in vec2 p3d_MultiTexCoord0;
in vec2 p3d_MultiTexCoord1;

out VertexData {
    vec4 p3d_Vertex;
    vec3 p3d_Normal;
    vec4 p3d_Color;
    vec2 p3d_MultiTexCoord0;
    vec2 p3d_MultiTexCoord1;
} outData;

void main()
{
    outData.p3d_Vertex = p3d_ModelViewMatrix * p3d_Vertex;
    outData.p3d_Normal = normalize(p3d_NormalMatrix * p3d_Normal);
    outData.p3d_Color = p3d_Color;
    outData.p3d_MultiTexCoord0 = p3d_MultiTexCoord0;
    outData.p3d_MultiTexCoord1 = p3d_MultiTexCoord1;

    gl_Position = p3d_ProjectionMatrix * outData.p3d_Vertex;
}
