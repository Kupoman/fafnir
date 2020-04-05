#version 330

uniform float foo;
void main()
{
    gl_Position = vec4(foo);
}
