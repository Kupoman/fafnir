#version 330

in vec3 origin;
in vec3 direction;

out vec4 out_origin;
out vec4 out_direction;

void main()
{
    out_origin.rgb = origin;
    out_origin.a = 1.0;

    out_direction.rgb = normalize(direction);
    out_direction.a = 1.0;
}
