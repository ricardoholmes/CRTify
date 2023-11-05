import overlay2
import tkinter as tk
from tkinter import ttk
import threading

overlay = None
rtRoot = None

def createUI():
    global overlay, rtRoot
    rtRoot = tk.Tk()
    rtRoot.title("CRTify Real time processor")
    rtRoot.geometry("150x100")
    rtRoot.config(background="White")
    rtRoot.columnconfigure(0, weight=1)
    rtRoot.rowconfigure(0,weight=1)

    def stop():
        overlay.stop()
        rtRoot.destroy()

    overlay = overlay2.Overlay2()
    olThread = threading.Thread(target=overlay.startVid)
    olThread.start()
    rtRoot.protocol("WM_DELETE_WINDOW",stop)
    stop_button = ttk.Button(rtRoot, text="Stop",command=stop)
    stop_button.grid(row=0,column=0, sticky='nesw')

    rtRoot.mainloop()


