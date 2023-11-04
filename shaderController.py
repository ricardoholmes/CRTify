import moderngl
from shader import ImageTransformer
import cv2

def applyShader(image: cv2.typing.MatLike, size: tuple[int, int]) -> cv2.typing.MatLike:
    ctx = moderngl.create_context(300, True, False)
    image_processor = ImageTransformer(ctx, size)

    # img = Image.fromarray(image)
    # texture = ctx.texture(img.size, 1, img.tobytes())
    texture = ctx.texture(image.shape[1::-1], image.shape[2], image)
    image_processor.render(texture)
    image_processor.write("output.png")

    return image_processor.get_image_cv2()

if __name__ == '__main__':
    image = cv2.imread('image.png')
    rendered = applyShader(image, (1280, 720))
    cv2.imwrite('test.png', rendered)
