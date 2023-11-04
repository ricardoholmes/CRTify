import moderngl
from array import array
import numpy as np
import cv2

class ImageTransformer:
    def __init__(self, ctx: moderngl.Context, size: tuple[int, int]):
        self.ctx = ctx
        self.size = size

        with open('shaders/VertexShader.glsl', 'r') as f:
            vert_shader = f.read()

        with open('shaders/FragmentShader.glsl', 'r') as f:
            frag_shader = f.read()

        self.program = self.ctx.program(
            vertex_shader = vert_shader,
            fragment_shader = frag_shader
        )

        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.size, 4)]
        )

        # fullscreen quad in NDC
        self.vertices = self.ctx.buffer(
            array(
                'f',
                [
                    # triangle strip creating a fullscreen quad
                    # x, y, u, v
                    -1,  1, 0, 1, # upper left
                    -1, -1, 0, 0, # lower left
                     1,  1, 1, 1, # upper right
                     1, -1, 1, 0, # lower right
                ]
            )
        )
        self.quad = self.ctx.vertex_array(
            self.program,
            [
                (self.vertices, '2f 2f', 'in_position', 'in_color'),
            ]
        )

    def render(self, texture: moderngl.Texture) -> cv2.typing.MatLike:
        self.fbo.use()
        texture.use(0)
        self.quad.render(mode=moderngl.TRIANGLE_STRIP)

    def get_image_cv2(self) -> cv2.typing.MatLike:
        raw = self.fbo.read(components=3, dtype='f1')
        buf = np.frombuffer(raw, dtype='uint8').reshape((*self.fbo.size[1::-1], 3))
        return buf
