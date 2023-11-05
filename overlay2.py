import cv2
import moderngl
from shader import ImageTransformer
from PIL import ImageGrab
import time
from pedalboard.io import AudioStream
import pedalboard
import pyaudio

class Overlay2:
    def __init__(self) -> None:

        size = (800,800)
        pos = (0,0)
        ctx = moderngl.create_context(460, True, False)
        transformer = ImageTransformer(ctx, size)
        self.fps = 30
        self.frame_time = int((1/self.fps) * 1000) # Frame time in milliseconds
        self.prevTime = time.time()

        while True:
            image = ImageGrab.grab((pos[0],pos[1],size[0],size[1])).convert('RGB')
            
            texture = ctx.texture(image.size, 3, image.tobytes())
            transformer.render(texture)
            crt_image = cv2.cvtColor(transformer.get_image_cv2(), cv2.COLOR_RGB2BGR)
            # crt_image = transformer.get_image_pil()

            cv2.imshow("CRTify", crt_image)

            now = time.time()
            delta = (now-self.prevTime)*1000
            self.prevTime = now
            if cv2.waitKey(int(max(self.frame_time-delta,1))) & 0xFF == ord('q'):
                break
    
    def audio_thread(self):
        # sr = 16000
        # chunk = 1 * sr
        # channel_nr = 1
        # audio_interface = pyaudio.PyAudio()
        # audio_stream = audio_interface.open()
        with AudioStream(input_device_name="alsa_output.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__sink.monitor") as stream:
            pass