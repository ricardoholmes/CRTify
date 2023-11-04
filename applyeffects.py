import cv2
import sys
import subprocess
from pedalboard import *
from pedalboard.io import AudioFile
import numpy as np
import shaderController

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
    fps = vid.get(cv2.CAP_PROP_FPS)
    frame_time = int((1/fps) * 1000) // 2 # Frame time in milliseconds
    output = cv2.VideoWriter("temp_video.mp4",cv2.VideoWriter_fourcc('m','p','4','v'), fps, dimensions)
    while True:
        ret, frame = vid.read()
        if not ret:
            break

        processed_frame = shaderController.applyShader(frame, dimensions)
        # cv2.imshow("Input", frame)
        # if cv2.waitKey(frame_time) & 0xFF == ord('q'):
        #     break
        # cv2.imshow("Debug",processed_frame)
        
        output.write(processed_frame)
    vid.release()
    output.release()

def audioEffects(filename):
    ext = filename.split(".")[-1]
    if '.mp4' in filename or '.avi' in filename:
        command = "ffmpeg -i "+ filename +" -ab 160k -ac 2 -ar 44100 -vn temp_audio.wav -y"
        subprocess.call(command, shell=True)
        filename = "temp_audio.wav"

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
    with AudioFile('processed_output.wav','w', samplerate, effected.shape[0]) as f:
        f.write(effected)

if __name__=="__main__":
    # audioEffects("test.mp3")
    vidEffects("test.mp4")