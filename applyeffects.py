import cv2
import sys, os
import subprocess
from pedalboard import *
from pedalboard.io import AudioFile
import shaderController
import threading
import shlex
import moderngl
from shader import ImageTransformer

def vidEffects(filepath:str):
    # Attempt to open input video
    try:
        vid = cv2.VideoCapture(filepath)
    except:
        print("Problem opening input stream")
        sys.exit(1)
    if not vid.isOpened():
        print("Capture stream not open")
        sys.exit(1)

    fps = vid.get(cv2.CAP_PROP_FPS)
    dimensions = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    ctx = moderngl.create_context(460, True, False)
    image_processor = ImageTransformer(ctx, dimensions)

    frame_time = int((1/fps) * 1000) # Frame time in milliseconds
    ret, frame = vid.read()
    # processed_frame = shaderController.applyShader(frame, dimensions)
    texture = ctx.texture(frame.shape[1::-1], frame.shape[2], frame)
    image_processor.render(texture)
    processed_frame = image_processor.get_image_cv2()
    new_dimensions = (processed_frame.shape[1], processed_frame.shape[0])
    output = cv2.VideoWriter("temp_video.mp4",cv2.VideoWriter_fourcc('m','p','4','v'), fps, new_dimensions)
    output.write(processed_frame)
    while True:
        ret, frame = vid.read()
        if not ret:
            break

        # processed_frame = shaderController.applyShader(frame, dimensions)
        texture = ctx.texture(frame.shape[1::-1], frame.shape[2], frame)
        image_processor.render(texture)
        processed_frame = image_processor.get_image_cv2()
        # cv2.imshow("Input", frame)
        # if cv2.waitKey(frame_time) & 0xFF == ord('q'):
        #     break
        # cv2.imshow("Debug",processed_frame)
        
        output.write(processed_frame)
        
    vid.release()
    output.release()
    cv2.destroyAllWindows()
    print("Video complete")

def audioEffects(filename):
    samplerate = 44100.0
    with AudioFile(filename).resampled_to(samplerate) as f:
        audio = f.read(f.frames)
    
    board = Pedalboard([
        # Resample(samplerate*0.65),
        Bitcrush(8),
        Compressor(-40,16,5,100),
        HighpassFilter(100),
        Distortion(),
    ])

    effected = board(audio, samplerate)
    with AudioFile('processed_audio.wav','w', samplerate, effected.shape[0]) as f:
        f.write(effected)
    print("Audio complete")

def applyAllEffects(filename:str, outfile:str, callback:callable=None):
    ext = filename.split(".")[-1]
    audio_filename = ""
    if ext == 'mp4' or ext == 'avi':
        command = "ffmpeg -i "+ shlex.quote(filename) +" -ab 160k -ac 2 -ar 44100 -vn temp_audio.wav -y"
        subprocess.call(command, shell=True)
        audio_filename = "temp_audio.wav"
    else:
        print("Bye bye")
        exit(1)
    
    print(audio_filename)
    # input()
    audio_thread = threading.Thread(target=audioEffects, args=(audio_filename,))
    video_thread = threading.Thread(target=vidEffects, args=(filename,))

    audio_thread.start()
    video_thread.start()

    audio_thread.join()
    video_thread.join()

    cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i processed_audio.wav -i temp_video.mp4 -pix_fmt yuv420p " + shlex.quote(outfile)
    subprocess.call(cmd, shell=True)

    local_path = os.getcwd()
    if os.path.exists(str(local_path) + "/temp_audio.wav"):
        os.remove(str(local_path) + "/temp_audio.wav")
    if os.path.exists(str(local_path) + "/processed_audio.wav"):
        os.remove(str(local_path) + "/processed_audio.wav")
    if os.path.exists(str(local_path) + "/temp_video.mp4"):
        os.remove(str(local_path) + "/temp_video.mp4")
    
    if callback != None:
        callback()

if __name__=="__main__":
    # audioEffects("test.mp3")
    # vidEffects("test.mp4")
    applyAllEffects("test.mp4", "output.mp4")
    # applyAllEffects("sample video.mp4", "sample output.mp4")