import tkinter as tk
import videoController as vidCon
import imageController as imgCon
import realtimeController as realCon

def create():
    root = tk.Tk()
    root.title("CRTify")
    root.geometry("400x300")
    root.config(background="White")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    tk.Button(root, text='IMAGE', command=imgCon.createUI).grid(row=0, column=0, sticky='nsew')
    tk.Button(root, text='VIDEO', command=vidCon.createUI).grid(row=0, column=1, sticky='nsew')
    tk.Button(root, text='REALTIME', command=realCon.createUI).grid(row=1, column=0, columnspan=2, sticky='nsew')

    root.mainloop()

if __name__=="__main__":
    create()
