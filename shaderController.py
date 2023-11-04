import moderngl
from shader import ImageTransformer
import cv2
from PIL import Image

ctx = -1
def applyShader(image: cv2.typing.MatLike, size: tuple[int, int]) -> cv2.typing.MatLike:
    global ctx
    if ctx == -1:
        ctx = moderngl.create_context(460, True, False)

    image_processor = ImageTransformer(ctx, size)

    texture = ctx.texture(image.shape[1::-1], image.shape[2], image)
    image_processor.render(texture)

    return image_processor.get_image_cv2()

def applyShaderPIL(image: Image.Image) -> Image.Image:
    global ctx
    if ctx == -1:
        ctx = moderngl.create_context(460, True, False)
        ctx.clear()

    image_processor = ImageTransformer(ctx, image.size)

    texture = ctx.texture(image.shape[1::-1], image.shape[2], image)
    image_processor.render(texture)

    return image_processor.get_image_cv2()

def clearContext():
    global ctx
    if ctx == -1:
        raise Exception('Attempted to clear context before creation')
    ctx.clear()
