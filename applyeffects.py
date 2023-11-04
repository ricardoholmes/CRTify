import cv2
import sys

def apply_effects(image):
    pass

def vidEffect(filepath:str):
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
    output = cv2.VideoWriter("temp_video.mp4",cv2.VideoWriter_fourcc('m','p','4','v'), fps, dimensions)
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        process_frame(frame)
        # output.write(frame)
    vid.release()
    output.release()
