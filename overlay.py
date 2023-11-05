import pygame
from pygame.locals import *
from PIL import Image, ImageTk, ImageGrab
from shader import ImageTransformer
import moderngl

FPS = 30
INVERSE_FPS = 1 / FPS

class Overlay:
    def __init__(self):
        self.kill = False
        self.current_image = -1

        ctx = moderngl.create_context(460, True, False)
        transformer = ImageTransformer(ctx, (400,400))
        
        pygame.init()
        screen = pygame.display.set_mode((450, 450), pygame.OPENGL | pygame.DOUBLEBUF)
        # screen = pygame.display.set_mode((450, 450))
        # surface = pygame.Surface(pygame.display.get_window_size())


        clock = pygame.time.Clock()
        while not self.kill:
            image = ImageGrab.grab((0,0,400,400)).convert('RGB')
            # image.save("test2.png")

            texture = ctx.texture(image.size, 3, image.tobytes())
            transformer.render(texture)
            # crt_image = transformer.get_image_cv2()
            crt_image = transformer.get_image_pil()
            crt_image.save("test2.png")

            # texture = ctx.texture(crt_image.size, 3, crt_image.tobytes())
            # texture.build_mipmaps()
            # texture.use()

            current_image = pygame.image.fromstring(crt_image.tobytes(), crt_image.size, crt_image.mode).convert()
            # pygame.image.save(screen, "test3.png")
            # current_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()
            # current_image = pygame.image.frombuffer(crt_image.tostring(), crt_image.shape[1::-1], "BGR")

            screen.fill(pygame.Color(255,255,255))
            # window.blit(current_image, (0, 0))
            screen.blit(current_image, current_image.get_rect())
            # pygame.Surface.blit(window, current_image, (0,0))
            pygame.display.flip()
            clock.tick(FPS)
            # pygame.time.wait(1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.stop()
                    break

        pygame.quit()

    def stop(self):
        self.kill = True
