import moderngl
from shader import ImageTransformer
import cv2

def applyShader(image: cv2.typing.MatLike, size: tuple[int, int]) -> cv2.typing.MatLike:
    ctx = moderngl.create_context(460, True, False)
    image_processor = ImageTransformer(ctx, size)

    texture = ctx.texture(image.shape[1::-1], image.shape[2], image)
    image_processor.render(texture)

    return image_processor.get_image_cv2()
