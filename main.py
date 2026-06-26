from tkinter import *
from PIL import Image, ImageTk
from how_btn import open_how_to_play
from play import open_play_menu
from theme import open_theme_menu

# main window
root = Tk()
root.title("Anime Tic Tac Toe")
try:
    root.iconbitmap("icon.ico")
except:
    pass

# fixed window size
width = 800
height = 450


root.geometry(f"{width}x{height}")
root.resizable(True, True)
root.aspect(16, 9, 16, 9)


# canvas for responsive UI
canvas = Canvas(root, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

import config

def load_theme_images():
    global original_bg, play_img_orig, how_img_orig, themes_img_orig, exit_img_orig
    theme = config.CURRENT_THEME
    
    try:
        original_bg = Image.open(f"img/BG/{theme}_bg.png")
    except:
        try:
            original_bg = Image.open("bgformode.png")
        except:
            original_bg = Image.new("RGB", (800, 450), "black")
        
    try:
        play_img_orig = Image.open(f"img/menu_buttons/{theme}/play_game.png")
        how_img_orig = Image.open(f"img/menu_buttons/{theme}/how_to_play.png")
        themes_img_orig = Image.open(f"img/menu_buttons/{theme}/themes.png")
        exit_img_orig = Image.open(f"img/menu_buttons/{theme}/exit.png")
    except Exception as e:
        print(f"Error loading theme images for {theme}:", e)
        # Fallback to Naruto if current theme buttons are missing
        try:
            play_img_orig = Image.open("img/menu_buttons/Naruto/play_game.png")
            how_img_orig = Image.open("img/menu_buttons/Naruto/how_to_play.png")
            themes_img_orig = Image.open("img/menu_buttons/Naruto/themes.png")
            exit_img_orig = Image.open("img/menu_buttons/Naruto/exit.png")
        except:
            play_img_orig = Image.new("RGBA", (200, 50), (255, 0, 0, 128))
            how_img_orig = Image.new("RGBA", (200, 50), (0, 255, 0, 128))
            themes_img_orig = Image.new("RGBA", (200, 50), (0, 0, 255, 128))
            exit_img_orig = Image.new("RGBA", (200, 50), (128, 128, 128, 128))

load_theme_images()

canvas.images = {}

def redraw_canvas(new_w, new_h):
    canvas._last_w = new_w
    canvas._last_h = new_h
    
    # resize background
    resized_bg = original_bg.resize((new_w, new_h))
    canvas.images['bg'] = ImageTk.PhotoImage(resized_bg)
    
    # resize buttons based on screen size ratio (e.g. 25% of width)
    btn_w = max(10, int(new_w * 0.25))
    btn_h = max(10, int(new_h * (50/450)))
    
    resized_play = play_img_orig.resize((btn_w, btn_h))
    canvas.images['play'] = ImageTk.PhotoImage(resized_play)
    
    resized_how = how_img_orig.resize((btn_w, btn_h))
    canvas.images['how'] = ImageTk.PhotoImage(resized_how)
    
    resized_themes = themes_img_orig.resize((btn_w, btn_h))
    canvas.images['themes'] = ImageTk.PhotoImage(resized_themes)

    resized_exit = exit_img_orig.resize((btn_w, btn_h))
    canvas.images['exit'] = ImageTk.PhotoImage(resized_exit)
    
    # redraw canvas elements
    canvas.delete("all")
    
    # add background
    canvas.create_image(0, 0, image=canvas.images['bg'], anchor="nw", tags="bg")
    
    # add buttons
    canvas.create_image(new_w/2, new_h * 0.55, image=canvas.images['play'], anchor="center", tags="play_btn")
    canvas.create_image(new_w/2, new_h * 0.67, image=canvas.images['how'], anchor="center", tags="how_btn")
    canvas.create_image(new_w/2, new_h*0.79, image=canvas.images['themes'], anchor="center", tags="themes_btn")
    canvas.create_image(new_w/2, new_h * 0.90, image=canvas.images['exit'], anchor="center", tags="exit_btn")

def resize_elements(event):
    if event.widget == canvas:
        new_w, new_h = event.width, event.height
        if new_w > 100 and new_h > 100:
            if getattr(canvas, '_last_w', 0) != new_w or getattr(canvas, '_last_h', 0) != new_h:
                redraw_canvas(new_w, new_h)

canvas.bind("<Configure>", resize_elements)

def on_theme_changed():
    load_theme_images()
    w, h = canvas.winfo_width(), canvas.winfo_height()
    if w > 100 and h > 100:
        redraw_canvas(w, h)

# click handlers
def on_play_click(event=None):
    open_play_menu(root)

def on_how_click(event=None):
    open_how_to_play(root)

def on_themes_click(event=None):
    open_theme_menu(root, on_theme_changed)

def on_exit_click(event=None):
    root.destroy()

# bind click events
canvas.tag_bind("play_btn", "<Button-1>", on_play_click)
canvas.tag_bind("how_btn", "<Button-1>", on_how_click)
canvas.tag_bind("themes_btn", "<Button-1>", on_themes_click)
canvas.tag_bind("exit_btn", "<Button-1>", on_exit_click)

# hover cursor effects
def on_enter(event):
    canvas.config(cursor="hand2")

def on_leave(event):
    canvas.config(cursor="")

for tag in ("play_btn", "how_btn", "themes_btn", "exit_btn"):
    canvas.tag_bind(tag, "<Enter>", on_enter)
    canvas.tag_bind(tag, "<Leave>", on_leave)


# press ESC to close fullscreen
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()