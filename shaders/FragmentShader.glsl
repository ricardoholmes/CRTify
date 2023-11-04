#version 460

uniform sampler2D image;
in vec2 color;
out vec3 out_color;

void main() {
    out_color = vec3(texture(image, color).rgb);
}

float scanline() {
    return 0.0;
}