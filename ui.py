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
        # applyeffects.applyAllEffects(curr_in, curr_out)
        
    # output_message.pack()

def createUI():
    global output_message, running
    window = tk.Tk()
    window.title("CRTify")
    window.geometry("400x400")
    window.config(background="White")

    input_file_button = ttk.Button(window, text="Open vid file", command=on_vid_open_button_pressed)
    output_file_button = ttk.Button(window, text="Save output file", command=on_vid_save_button_pressed)

    output_message = StringVar(value="")
    run_button = ttk.Button(window, text="Run CRTify", command=run_crtify)
    output_label = ttk.Label(window, textvariable=output_message, background="White")

    input_file_button.pack()
    output_file_button.pack()
    run_button.pack()
    output_label.pack()

    window.mainloop()
    running = False
    if threading.active_count() > 1:
        for i in threading.enumerate():
            if i != threading.current_thread():
                i.join()

if __name__=="__main__":
    createUI()