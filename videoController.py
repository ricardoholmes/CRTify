import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import filedialog as fd
import os
import applyeffects
import threading

curr_dir = os.path.expanduser("~")
curr_in = ""
curr_out = ""
output_message = None
running = True

def on_vid_open_button_pressed():
    global curr_dir, curr_in
    filename = fd.askopenfilename(
        title="Open source video",
        initialdir=curr_dir,
        filetypes=(
            ("mp4 files","*.mp4"),
        )
    )
    if filename:
        curr_dir = filename.split("/")[:-1]
        curr_in = filename
    print(filename)

def on_vid_save_button_pressed():
    global curr_dir, curr_out
    filename = fd.asksaveasfilename(
        title="Output video",
        initialdir=curr_dir,
        filetypes=(
            ("mp4 files","*.mp4"),
            ("avi files","*.avi"),
        )
    )
    if filename:
        curr_dir = filename.split("/")[:-1]
        curr_out = filename
    print(filename)

def on_crtify_complete():
    global running
    if running:
        output_message.set("Success!")

def run_crtify():
    global curr_in, curr_out, output_message

    if curr_in=="":
        output_message.set("No input file selected")
    elif curr_out=="":
        output_message.set("No output file selected")
    else:
        #run
        processing_thread = threading.Thread(target=applyeffects.applyAllEffects, args=(curr_in, curr_out, on_crtify_complete,))
        processing_thread.start()
        createRunningUI()
        # applyeffects.applyAllEffects(curr_in, curr_out)
        
    # output_message.pack()

def createUI():
    global output_message, running
    window = tk.Tk()
    window.title("CRTify")
    window.geometry("400x400")
    window.config(background="White")

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)

    input_file_button = ttk.Button(window, text="Open video file", command=on_vid_open_button_pressed)
    output_file_button = ttk.Button(window, text="Save output file", command=on_vid_save_button_pressed)

    output_message = StringVar(value="")
    run_button = ttk.Button(window, text="Run CRTify", command=run_crtify)
    output_label = ttk.Label(window, textvariable=output_message, background="White")

    input_file_button.grid(row=0, column=0, sticky='nsew')
    output_file_button.grid(row=0, column=1, sticky='nsew')
    run_button.grid(row=1, column=0, columnspan=2, sticky='nsew')
    output_label.grid(row=2, column=0, columnspan=2, sticky='nsew')

    window.mainloop()

    running = False
    if threading.active_count() > 1:
        for i in threading.enumerate():
            if i != threading.current_thread():
                i.join()

def createRunningUI():
    global audioProgress, videoProgress, stitchingProgress, doneButton
    root = tk.Tk()
    root.title("CRTify Video Processor")
    root.geometry("200x300")
    root.config(background="White")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=1)
    root.rowconfigure(6, weight=1)

    tk.Label(root, text='Processing Audio').grid(row=0, column=0, sticky='nsew')
    audioProgress = ttk.Progressbar(root, mode='determinate')
    audioProgress.grid(row=1, column=0, sticky='nsew')

    tk.Label(root, text='Processing Video').grid(row=2, column=0, sticky='nsew')
    videoProgress = ttk.Progressbar(root, mode='determinate')
    videoProgress.grid(row=3, column=0, sticky='nsew')

    tk.Label(root, text='Re-stitching Video').grid(row=4, column=0, sticky='nsew')
    stitchingProgress = ttk.Progressbar(root, mode='determinate')
    stitchingProgress.grid(row=5, column=0, sticky='nsew')

    doneButton = tk.Button(root, text='DONE', command=root.withdraw)

    root.mainloop()

if __name__=="__main__":
    createUI()
