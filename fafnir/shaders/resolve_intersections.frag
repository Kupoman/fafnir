#version 330

/*
uniform samplerBuffer buffer_vertices;
uniform isamplerBuffer buffer_primitives;
uniform samplerBuffer buffer_materials;

uniform mat4 p3d_ViewMatrix;
uniform mat3 p3d_NormalMatrix;

flat in int instance_id;

struct {
    vec4 ambient;
    vec4 diffuse;
    vec4 emission;
    vec3 specular;
    float shininess;
} p3d_Material;

vec4 p3d_Vertex = vec4(0.0);
vec3 p3d_Normal = vec3(0.0);
vec4 p3d_Color = vec4(0.0);
vec2 p3d_MultiTexCoord0 = vec2(0.0);
vec2 p3d_MultiTexCoord1 = vec2(0.0);

vec3 _unpack_normal(vec4 vdata1)
{
    vec3 normal;
    normal.xy = unpackSnorm2x16(floatBitsToUint(vdata1.x));
    normal.z = unpackSnorm2x16(floatBitsToUint(vdata1.y)).x;
    return normal;
}

void fafnir_unpack_fragment()
{
    ivec2 texel_pos = ivec2(gl_FragCoord.xy);
    vec4 data = texelFetch(texture_intersections, texel_pos, 0);
    vec3 uvw = vec3(data.x, data.y, 1.0 - data.x - data.y);
    int primid = int(data.z);
    int materialid = int(data.w - 1.0);

    if (instance_id != materialid) {
        discard;
    }

    int v0_idx = texelFetch(buffer_primitives, int(primid+0)).x;
    vec4 v0_data0 = texelFetch(buffer_vertices, int(v0_idx)).bgra;
    int v1_idx = texelFetch(buffer_primitives, int(primid+1)).x;
    vec4 v1_data0 = texelFetch(buffer_vertices, int(v1_idx)).bgra;
    int v2_idx = texelFetch(buffer_primitives, int(primid+2)).x;
    vec4 v2_data0 = texelFetch(buffer_vertices, int(v2_idx)).bgra;

    p3d_Vertex += uvw.x * vec4(v0_data0.xyz, 0.0);
    p3d_Vertex += uvw.y * vec4(v1_data0.xyz, 0.0);
    p3d_Vertex += uvw.z * vec4(v2_data0.xyz, 0.0);

    vec4 v0_data1 = texelFetch(buffer_vertices, int(v0_idx+1)).bgra;
    vec4 v1_data1 = texelFetch(buffer_vertices, int(v1_idx+1)).bgra;
    vec4 v2_data1 = texelFetch(buffer_vertices, int(v2_idx+1)).bgra;

    p3d_Normal += uvw.x * _unpack_normal(v0_data1);
    p3d_Normal += uvw.y * _unpack_normal(v1_data1);
    p3d_Normal += uvw.z * _unpack_normal(v2_data1);
    p3d_Normal = normalize(p3d_Normal);

    p3d_Color += uvw.x * unpackUnorm4x8(int(v0_data0.w));
    p3d_Color += uvw.y * unpackUnorm4x8(int(v1_data0.w));
    p3d_Color += uvw.z * unpackUnorm4x8(int(v2_data0.w));

    p3d_MultiTexCoord0 += uvw.x * unpackUnorm2x16(floatBitsToUint(v0_data1.z));
    p3d_MultiTexCoord0 += uvw.y * unpackUnorm2x16(floatBitsToUint(v0_data1.z));
    p3d_MultiTexCoord0 += uvw.z * unpackUnorm2x16(floatBitsToUint(v0_data1.z));

    p3d_MultiTexCoord1 += uvw.x * unpackUnorm2x16(floatBitsToUint(v0_data1.w));
    p3d_MultiTexCoord1 += uvw.y * unpackUnorm2x16(floatBitsToUint(v0_data1.w));
    p3d_MultiTexCoord1 += uvw.z * unpackUnorm2x16(floatBitsToUint(v0_data1.w));
}

void fafnir_unpack_material()
{
    int material_index = instance_id * 4;
    p3d_Material.ambient = texelFetch(buffer_materials, material_index + 0);
    p3d_Material.diffuse = texelFetch(buffer_materials, material_index + 1);
    p3d_Material.emission = texelFetch(buffer_materials, material_index + 2);

    vec4 specular_data = texelFetch(buffer_materials, material_index + 3);
    p3d_Material.specular = specular_data.xyz;
    p3d_Material.shininess = specular_data.w;
}

uniform struct p3d_LightSourceParameters {
    vec4 position;
} p3d_LightSource[8];
*/

uniform sampler2D texture_intersections;
out vec4 frag_out;

void main()
{
    ivec2 texel_pos = ivec2(gl_FragCoord.xy);
    vec4 data = texelFetch(texture_intersections, texel_pos, 0);
    frag_out.rgb = data.xyz;
    frag_out.a = 1.0;

    /*
    fafnir_unpack_fragment();
    fafnir_unpack_material();

    vec3 light_pos = p3d_LightSource[0].position.xyz;
    vec3 V = normalize(-p3d_Vertex.xyz);
    vec3 N = p3d_Normal;
    vec3 L = normalize(light_pos - p3d_Vertex.xyz);
    vec3 H = normalize(L + V);
    float NoL = dot(N, L);
    float NoH = dot(N, H);

    vec3 diffuse = NoL * p3d_Material.diffuse.rgb;
    vec3 specular = max(pow(NoH, p3d_Material.shininess), 0.0) * p3d_Material.specular.rgb;

    frag_out.rgb = diffuse + specular;

    frag_out.w = 1.0;
    */
}
