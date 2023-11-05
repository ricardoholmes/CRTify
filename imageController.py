import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import filedialog as fd
import os
import shaderController
from PIL import Image

curr_dir = os.path.expanduser("~")
curr_in = ""
curr_out = ""
output_message = None
running = True

def on_vid_open_button_pressed():
    global curr_dir, curr_in
    filename = fd.askopenfilename(
        title="Open source image",
        initialdir=curr_dir,
        filetypes=(
            ("png files","*.png"),
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
            ("png files","*.png"),
            ("jpg files","*.jpg"),
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
        image = Image.open(curr_in)
        shaderImage = shaderController.applyShaderPIL(image.convert("RGB"))
        shaderImage.save(curr_out)
        on_crtify_complete()

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

    input_file_button = ttk.Button(window, text="Open image file", command=on_vid_open_button_pressed)
    output_file_button = ttk.Button(window, text="Save output file", command=on_vid_save_button_pressed)

    output_message = StringVar(value="")
    run_button = ttk.Button(window, text="Run CRTify", command=run_crtify)
    output_label = ttk.Label(window, textvariable=output_message, background="White", anchor='center')

    input_file_button.grid(row=0, column=0, sticky='nsew')
    output_file_button.grid(row=0, column=1, sticky='nsew')
    run_button.grid(row=1, column=0, columnspan=2, sticky='nsew')
    output_label.grid(row=2, column=0, columnspan=2, sticky='nsew')

    window.mainloop()

if __name__=="__main__":
    createUI()
