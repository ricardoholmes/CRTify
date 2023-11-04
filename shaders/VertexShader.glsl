#version 430

in vec2 vertex_pos;
in vec2 in_texture;

out vec2 v_texture;

void main() {
   gl_Position = vec4(vertex_pos, 0.0, 1.0);
   v_texture = in_texture;
}
