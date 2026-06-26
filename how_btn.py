from tkinter import *
from PIL import Image, ImageTk
import config

def open_how_to_play(root):

    how_window = Frame(root)
    how_window.place(x=0, y=0, relwidth=1, relheight=1)

    theme = config.CURRENT_THEME
    try:
        original_img = Image.open(f"img/how_to_play_btn/{theme}_ins.png")
        
    except:
        original_img = Image.open("how.png")

    label = Label(how_window)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    back_btn = Button(how_window,
                      text="← BACK",
                      font=("Orbitron", 14, "bold"),
                      fg="white",
                      bg="black",
                      command=how_window.destroy)

    back_btn.place(x=30, y=30)

    def resize_how(event):
        if event.widget == how_window:
            new_w, new_h = event.width, event.height
            if new_w > 100 and new_h > 100:
                if getattr(how_window, '_last_w', 0) != new_w or getattr(how_window, '_last_h', 0) != new_h:
                    how_window._last_w = new_w
                    how_window._last_h = new_h
                    resized = original_img.resize((new_w, new_h))
                    how_window.bg_img = ImageTk.PhotoImage(resized)
                    label.config(image=how_window.bg_img)

    how_window.bind("<Configure>", resize_how)