#version 430

precision mediump float;
uniform sampler2D Texture;

in vec2 v_texture;
out vec4 color;

void main() {
  color = vec4(texture(Texture, v_texture).rgb, 1.0);
}