import tkinter
from PIL import Image, ImageTk, ImageGrab
from shaderController import applyShader
from time import sleep
from threading import Thread

FPS = 30
INVERSE_FPS = 1 / FPS

class Overlay:
    def __init__(self):
        self.kill = False
        self.root = tkinter.Tk()

        self.w = self.root.winfo_screenwidth() // 4
        self.h = self.root.winfo_screenheight() // 4
        self.root.overrideredirect(1)

        w = self.w
        h = self.h

        self.root.geometry(f'{w}x{h}+0+0')
        self.root.focus_set()
        self.root.bind("<Escape>", lambda x: self.stop())
        self.canvas = tkinter.Canvas(self.root,width=w,height=h)
        self.canvas.pack()
        self.canvas.configure(background='black')

        self.runner = Thread(target=self.run)
        self.runner.start()

        self.root.mainloop()

    def run(self):
        while not self.kill:
            self.clear_image()
            image = screenshot()
            crt_image = applyShader(image)
            self.set_image(crt_image)
            sleep(INVERSE_FPS)

    def clear_image(self):
        self.canvas.delete('all')

    def set_image(self, pilImage: Image.Image):
        image = ImageTk.PhotoImage(pilImage)
        self.canvas.create_image(self.w/2, self.h/2, image=image)

    def stop(self):
        self.kill = True
        if self.root == 0:
            raise Exception('Attempted to stop overlay before starting')
        self.root.destroy()
        self.root = 0

def screenshot() -> Image.Image:
    image = ImageGrab.grab(bbox=None, xdisplay=None)
    return image
