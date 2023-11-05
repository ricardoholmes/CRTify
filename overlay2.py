import cv2
import moderngl
from shader import ImageTransformer
from PIL import ImageGrab
import time, os
from pedalboard.io import AudioStream
from pedalboard import *
import threading
from ffpyplayer.player import MediaPlayer

class Overlay2:
    def __init__(self) -> None:
        # self.audio_thread()     
        audio_thread = threading.Thread(target=self.audio_thread, daemon=True)
        audio_thread.start() 
        self.size = (1920,1080)
        self.pos = (0,0)
        self.fps = 30
        self.frame_time = int((1/self.fps) * 1000) # Frame time in milliseconds
        self.prevTime = time.time()
        
    def startVid(self):
        self.running = True
        ctx = moderngl.create_context(460, True, False)
        transformer = ImageTransformer(ctx, self.size)
        crt_image = None
        cv2.namedWindow('CRTify', cv2.WINDOW_AUTOSIZE)
        while True:
            image = ImageGrab.grab((self.pos[0],self.pos[1],self.size[0],self.size[1])).convert('RGB')

            texture = ctx.texture(image.size, 3, image.tobytes())
            transformer.render(texture)
            crt_image = cv2.cvtColor(transformer.get_image_cv2(), cv2.COLOR_RGB2BGR)
            # crt_image = transformer.get_image_pil()

            cv2.imshow("CRTify", crt_image)

            now = time.time()
            delta = (now-self.prevTime)*1000
            self.prevTime = now
            if cv2.waitKey(int(max(self.frame_time-delta,1))) & 0xFF == ord('q') or not self.running:
                break
            
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        cv2.destroyAllWindows()
    
    def audio_thread(self):
        stream = AudioStream(input_device_name="CABLE Output (VB-Audio Virtual", 
                         output_device_name="Speakers (Realtek(R) Audio)")
        stream.plugins = Pedalboard([
            # Resample(samplerate*0.65),
            Bitcrush(8),
            Compressor(-40,16,5,100),
            HighpassFilter(100),
            LowpassFilter(4000),
            Distortion(),
        ])

        self.player = MediaPlayer("static.mp3", ff_opts={'loop':0})
        
        stream.run()

    def stop(self):
        self.running = False
        