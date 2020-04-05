#version 330

//#extension GL_ARB_bindless_texture : enable
//sampler2D p3d_Texture0;
//flat in int instance_id;
//void unpack_texture() {
//    vec4 texture_data = texelFetch(buffer_materials, material_index + 4);
//    uvec2 handle;
//    handle.x = uint(floatBitsToInt(texture_data.x));
//    handle.y = uint(floatBitsToInt(texture_data.y));
//    p3d_Texture0 = sampler2D(handle);
//}

uniform sampler2D p3d_Texture0;
uniform int instance_id;
void unpack_texture() {}

uniform samplerBuffer buffer_meshes;
uniform samplerBuffer buffer_materials;

vec4 p3d_Vertex = vec4(0.0);
vec3 p3d_Normal = vec3(0.0);
vec2 p3d_MultiTexCoord0 = vec2(0.0);

struct {
    vec4 ambient;
    vec4 diffuse;
    vec4 emission;
    vec3 specular;
    float shininess;
} p3d_Material;


uniform struct p3d_LightSourceParameters {
    vec4 position;
} p3d_LightSource[8];

uniform sampler2D texture_intersections;
out vec4 frag_out;

vec2 bary_interp_vec2(vec2 a, vec2 b, vec2 c, vec3 uvw)
{
    vec2 final = vec2(0.0);
    final += uvw.x * a;
    final += uvw.y * b;
    final += uvw.z * c;
    return final;
}

vec3 bary_interp_vec3(vec3 a, vec3 b, vec3 c, vec3 uvw)
{
    vec3 final = vec3(0.0);
    final += uvw.x * a;
    final += uvw.y * b;
    final += uvw.z * c;
    return final;
}

void fafnir_unpack_vertex()
{
    ivec2 texel_pos = ivec2(gl_FragCoord.xy);
    vec4 data = texelFetch(texture_intersections, texel_pos, 0);

    int materialid = int(data.w - 1.0);
    //if (instance_id != materialid) {
    //    discard;
    //}

    vec3 uvw = vec3(data.xy, 1.0 - data.x - data.y);

    int vertexStride = 4;
    int vertexIdBase = int(data.z * 3 * vertexStride);
    vec3 v0 = texelFetch(buffer_meshes, vertexIdBase + 0).xyz;
    vec3 n0 = texelFetch(buffer_meshes, vertexIdBase + 1).xyz;
    vec2 t0 = texelFetch(buffer_meshes, vertexIdBase + 2).xy;
    vec3 v1 = texelFetch(buffer_meshes, vertexIdBase + 4).xyz;
    vec3 n1 = texelFetch(buffer_meshes, vertexIdBase + 5).xyz;
    vec2 t1 = texelFetch(buffer_meshes, vertexIdBase + 6).xy;
    vec3 v2 = texelFetch(buffer_meshes, vertexIdBase + 8).xyz;
    vec3 n2 = texelFetch(buffer_meshes, vertexIdBase + 9).xyz;
    vec2 t2 = texelFetch(buffer_meshes, vertexIdBase + 10).xy;

    p3d_Vertex = vec4(bary_interp_vec3(v0, v1, v2, uvw), 1.0);
    p3d_Normal = bary_interp_vec3(n0, n1, n2, uvw);
    p3d_MultiTexCoord0 = bary_interp_vec2(t0, t1, t2, uvw);
}

void fafnir_unpack_material()
{
    int material_index = instance_id * 5;
    p3d_Material.ambient = texelFetch(buffer_materials, material_index + 0);
    p3d_Material.diffuse = texelFetch(buffer_materials, material_index + 1);
    p3d_Material.emission = texelFetch(buffer_materials, material_index + 2);

    vec4 specular_data = texelFetch(buffer_materials, material_index + 3);
    p3d_Material.specular = specular_data.xyz;
    p3d_Material.shininess = specular_data.w;

    unpack_texture();
}

void main()
{
    fafnir_unpack_vertex();
    fafnir_unpack_material();

    vec3 light_pos = p3d_LightSource[0].position.xyz;
    vec3 V = normalize(-p3d_Vertex.xyz);
    vec3 N = p3d_Normal;
    vec3 L = normalize(light_pos - p3d_Vertex.xyz);
    vec3 H = normalize(L + V);
    float NoL = dot(N, L);
    float NoH = dot(N, H);

    vec3 base_color = p3d_Material.diffuse.rgb;
    if (textureSize(p3d_Texture0, 0).x > 0) {
        base_color *= texture(p3d_Texture0, p3d_MultiTexCoord0).rgb;
    }
    vec3 diffuse = NoL * base_color;
    vec3 specular = max(pow(NoH, p3d_Material.shininess), 0.0) * p3d_Material.specular.rgb;

    frag_out.rgb = diffuse + specular;
    frag_out.w = 1.0;
    frag_out.rgb = vec3(NoL);
}
