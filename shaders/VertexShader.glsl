#version 460

in vec2 in_coord;
in vec2 in_texture;

// out vec2 flagCoord;
out vec2 fragTexture;

void main() {
    gl_Position = vec4(in_coord, 0.0, 1.0);

    // flagCoord = in_coord;
    fragTexture = in_texture;
}
