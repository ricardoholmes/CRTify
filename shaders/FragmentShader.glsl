#version 330

uniform sampler2D image;
in vec2 color;
out vec4 out_color;

void main() {
    out_color = vec4(texture(image, color).rgb, 1);
}
