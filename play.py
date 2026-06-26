from tkinter import *
from PIL import Image, ImageTk
import config
from game import start_game

def open_play_menu(root):

    # create new frame
    win = Frame(root)
    win.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------------- background & button original images ----------------
    theme = config.CURRENT_THEME
    
    try:
        original_bg = Image.open(f"img/mode/{theme}_mode.png")
    except:
        original_bg = Image.open("bgformode.png")
        
    try:
        # Load theme-specific back button or fallback to general back button
        original_back = Image.open(f"img/back/{theme}_back.png")
    except:
        try:
            original_back = Image.open("img/menu_buttons/back.png")
        except:
            original_back = None

    bg_canvas = Canvas(win, highlightthickness=0, bg="black")
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    win.images = {}

    def single_player():
        start_game(root, mode="single")

    def two_player():
        start_game(root, mode="double")

    def go_back():
        win.destroy()

    def on_click(event):
        w = bg_canvas.winfo_width()
        h = bg_canvas.winfo_height()
        
        if w == 0 or h == 0:
            return
            
        rel_x = event.x / w
        rel_y = event.y / h
        
        # 🔵 Using relative coordinates so the clickable areas scale correctly
        # LEFT BOX (Single Player) roughly 5% to 45% width, 30% to 85% height
        if 0.05 <= rel_x <= 0.45 and 0.30 <= rel_y <= 0.85:
            single_player()
            
        # 🔵 RIGHT BOX (Two Player) roughly 50% to 95% width, 30% to 85% height
        elif 0.50 <= rel_x <= 0.95 and 0.30 <= rel_y <= 0.85:
            two_player()

    def on_enter_cursor(e):
        bg_canvas.config(cursor="hand2")

    def on_leave_cursor(e):
        bg_canvas.config(cursor="")

    # Create elements
    bg_canvas.create_image(0, 0, anchor="nw", tags="bg")
    bg_canvas.tag_bind("bg", "<Button-1>", on_click)
    
    if original_back:
        back_id = bg_canvas.create_image(0, 0, anchor="nw", tags="back")
    else:
        back_id = bg_canvas.create_text(0, 0, text="← BACK", font=("Arial", 14, "bold"), fill="white", anchor="nw", tags="back")

    bg_canvas.tag_bind(back_id, "<Button-1>", lambda e: go_back())
    bg_canvas.tag_bind(back_id, "<Enter>", on_enter_cursor)
    bg_canvas.tag_bind(back_id, "<Leave>", on_leave_cursor)

    # ---------------- responsive resizing ----------------
    def resize_play(event):
        if event.widget == bg_canvas:
            w, h = event.width, event.height
            if w > 100 and h > 100:
                if getattr(win, '_last_w', 0) != w or getattr(win, '_last_h', 0) != h:
                    win._last_w = w
                    win._last_h = h
                    
                    resized_bg = original_bg.resize((w, h))
                    win.images['bg'] = ImageTk.PhotoImage(resized_bg)
                    bg_canvas.itemconfig("bg", image=win.images['bg'])
                    
                    btn_w = max(50, int(w * 0.12))
                    btn_h = max(25, int(h * 0.08))
                    
                    bg_canvas.coords("back", w*0.05, h*0.05)
                    
                    if original_back:
                        resized_back = original_back.resize((btn_w, btn_h))
                        win.images['back'] = ImageTk.PhotoImage(resized_back)
                        bg_canvas.itemconfig("back", image=win.images['back'])

    bg_canvas.bind("<Configure>", resize_play)
