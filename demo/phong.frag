#version 330

uniform mat4 p3d_ViewMatrix;
uniform mat3 p3d_NormalMatrix;

uniform sampler2D p3d_Texture0;

uniform struct {
    vec4 ambient;
    vec4 diffuse;
    vec4 emission;
    vec3 specular;
    float shininess;
} p3d_Material;

uniform struct p3d_LightSourceParameters {
    vec4 position;
} p3d_LightSource[8];

in VertexData {
    vec4 p3d_Vertex;
    vec3 p3d_Normal;
    vec4 p3d_Color;
    vec2 p3d_MultiTexCoord0;
    vec2 p3d_MultiTexCoord1;
};

out vec4 fragOut;

vec3 toLinear(vec3 color) {
    return pow(color, vec3(2.2));
}

vec3 toSrgb(vec3 color) {
    return pow(color, vec3(1/2.2));
}

vec3 getDiffuseColor() {
    vec3 factor = p3d_Material.diffuse.rgb;
    vec3 textureColor = texture(p3d_Texture0, p3d_MultiTexCoord0).rgb;
    vec3 color = factor * textureColor;
    return toLinear(color);
}

vec3 getSpecularColor() {
    vec3 factor = p3d_Material.specular.rgb;
    return toLinear(factor);
}

void main()
{
    vec3 V = normalize(-p3d_Vertex.xyz);
    vec3 N = p3d_Normal;

    vec3 light_pos = p3d_LightSource[0].position.xyz;
    vec3 L = normalize(light_pos - p3d_Vertex.xyz);
    vec3 H = normalize(L + V);

    float NoL = dot(N, L);
    float NoH = dot(N, H);

    vec3 diffuseColor = getDiffuseColor();
    vec3 specularColor = getSpecularColor();

    vec3 diffuse = NoL * diffuseColor;
    vec3 specular = max(pow(NoH, p3d_Material.shininess), 0.0) * specularColor;

    fragOut.rgb = toSrgb(diffuse + specular);
    fragOut.w = 1.0;
}
