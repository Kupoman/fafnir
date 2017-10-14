#version 420

uniform samplerBuffer buffer_vertices;
uniform isamplerBuffer buffer_primitives;
/*uniform isamplerBuffer material_indexes;*/
/*uniform samplerBuffer material_cache;*/
uniform sampler2D texture_intersections;

uniform mat4 p3d_ViewMatrix;
uniform mat3 p3d_NormalMatrix;

uniform p3d_LightSourceParameters {
    vec4 position;
} p3d_LightSource[1];

flat in int instance_id;
out vec4 frag_out;

vec3 unpack_normal(vec4 vdata1)
{
    vec3 normal;
    normal.xy = unpackSnorm2x16(floatBitsToUint(vdata1.x));
    normal.z = unpackSnorm2x16(floatBitsToUint(vdata1.y)).x;
    return normal;
}

void main()
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

    vec4 position = vec4(0.0, 0.0, 0.0, 1.0);
    position += uvw.x * vec4(v0_data0.xyz, 0.0);
    position += uvw.y * vec4(v1_data0.xyz, 0.0);
    position += uvw.z * vec4(v2_data0.xyz, 0.0);
    
    vec4 v0_data1 = texelFetch(buffer_vertices, int(v0_idx+1)).bgra;
    vec4 v1_data1 = texelFetch(buffer_vertices, int(v1_idx+1)).bgra;
    vec4 v2_data1 = texelFetch(buffer_vertices, int(v2_idx+1)).bgra;

    vec3 normal = vec3(0.0);
    normal += uvw.x * unpack_normal(v0_data1);
    normal += uvw.y * unpack_normal(v1_data1);
    normal += uvw.z * unpack_normal(v2_data1);
    normal = normalize(normal);

    // vec4 material_data = texelFetch(material_cache, materialid);
    // vec4 diffuse = material_data;
    vec4 diffuse = vec4(0.8, 0.8, 0.8, 1.0);

    vec3 light_pos = p3d_LightSource[0].position.xyz;
    vec3 light_vec = normalize(light_pos - position.xyz);
    float nol = dot(normal, light_vec);

    frag_out.xyz = nol*diffuse.rgb;
    frag_out.w = 1.0;
}
