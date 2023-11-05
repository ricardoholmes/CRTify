import os
import sys
import pygame
from PIL import Image, ImageTk, ImageGrab
from shader import ImageTransformer
from time import sleep
from threading import Thread
import moderngl
import numpy as np

FPS = 30
INVERSE_FPS = 1 / FPS

class Overlay:
    def __init__(self):
        self.kill = False
        self.current_image = -1

        pygame.init()
        window = pygame.display.set_mode((0, 0), pygame.OPENGL)
        surface = pygame.Surface(pygame.display.get_window_size())

        ctx = moderngl.create_context(460, True, False)
        transformer = ImageTransformer(ctx, pygame.display.get_window_size())

        clock = pygame.time.Clock()
        while not self.kill:
            image = ImageGrab.grab().convert('RGBA')

            texture = ctx.texture(image.size, 4, image.tobytes())
            transformer.render(texture)
            crt_image = transformer.get_image_pil()

            # texture = ctx.texture(crt_image.size, 3, crt_image.tobytes())
            # texture.build_mipmaps()
            # texture.use()

            current_image = pygame.image.fromstring(crt_image.tobytes(), crt_image.size, crt_image.mode).convert()

            window.fill(0)
            window.blit(current_image, (0, 0))
            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.stop()
                    break

        pygame.quit()

    def stop(self):
        self.kill = True
