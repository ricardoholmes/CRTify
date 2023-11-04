#version 330

in vec2 in_position;
in vec2 in_color;
out vec2 color;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    color = in_color;
}
