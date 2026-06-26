from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import config

def open_theme_menu(root, on_theme_changed_callback=None):

    # create new frame
    win = Frame(root)
    win.place(x=0, y=0, relwidth=1, relheight=1)

    bg_canvas = Canvas(win, highlightthickness=0, bg="black")
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    scrollbar = Scrollbar(win, orient="vertical", command=bg_canvas.yview)
    scrollbar.place(relx=1.0, rely=0.0, relheight=1.0, anchor="ne")

    def update_fixed_elements():
        y = bg_canvas.canvasy(0)
        bg_canvas.coords("bg", 0, y)
        w = bg_canvas.winfo_width()
        h = bg_canvas.winfo_height()
        if w > 10 and h > 10:
            bg_canvas.coords("title", w/2, y + h * 0.12)
            bg_canvas.coords("back", w*0.05, y + h * 0.05)
            bg_canvas.coords("coins", w*0.95, y + h * 0.05)

    def on_yscroll(*args):
        scrollbar.set(*args)
        update_fixed_elements()
        
    bg_canvas.configure(yscrollcommand=on_yscroll)

    def _on_mousewheel(event):
        bg_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        update_fixed_elements()

    # Load original images safely
    try:
        original_bg = Image.open("bgformode.png")
    except:
        original_bg = None

    try:
        original_back = Image.open("img/menu_buttons/back.png")
    except:
        original_back = None

    win.images = {}
    
    def back_main():
        bg_canvas.unbind_all("<MouseWheel>")
        win.destroy()

    def on_enter_cursor(e):
        bg_canvas.config(cursor="hand2")

    def on_leave_cursor(e):
        bg_canvas.config(cursor="")

    # Create fixed elements
    bg_canvas.create_image(0, 0, anchor="nw", tags="bg")
    bg_canvas.create_text(0, 0, text="Select Theme", font=("Times New Roman", 40, "bold"), fill="#c22c3e", tags="title")
    bg_canvas.create_text(0, 0, text=f"Coins: {config.COINS}", font=("Arial", 16, "bold"), fill="gold", anchor="ne", tags="coins")
    
    if original_back:
        back_id = bg_canvas.create_image(0, 0, anchor="nw", tags="back")
    else:
        back_id = bg_canvas.create_text(0, 0, text="← BACK", font=("Arial", 14, "bold"), fill="white", anchor="nw", tags="back")
        
    bg_canvas.tag_bind(back_id, "<Button-1>", lambda e: back_main())
    bg_canvas.tag_bind(back_id, "<Enter>", on_enter_cursor)
    bg_canvas.tag_bind(back_id, "<Leave>", on_leave_cursor)

    themes = [
        "Arsene_Lupin", "Astro_Boy", "Asuka", "Dio_Brando","Doraemon", "Edward_Elric",
        "Gojo_Satoru", "Gon_Freecss", "Guts", "Himmel", "Hinata_Hyuga",
        "Ichigo_Kurosaki", "Lelouch", "Levi_Ackermen", "Light_Yagami", "Luffy",
        "Mikasa", "Motoko_Kusanagi", "Naruto", "Nezuko", "pokemon",
        "Sailor_Moon", "Saitama","Shoyo_Hinata", "Son_Goku", "Spike_Spiegel", "Tanjiro",
        "Tenchi_Muyo"
    ]

    def theme_click(t):
        if t in config.UNLOCKED_THEMES:
            config.save_theme(t)
            if on_theme_changed_callback:
                on_theme_changed_callback()
        else:
            if config.COINS >= 100:
                confirm = messagebox.askyesno("Unlock Theme", f"Do you want to spend 100 coins to unlock the {t.replace('_', ' ')} theme?")
                if confirm:
                    if config.unlock_theme(t):
                        # Successfully unlocked
                        messagebox.showinfo("Unlocked", f"You unlocked the {t.replace('_', ' ')} theme!")
                        bg_canvas.itemconfig("coins", text=f"Coins: {config.COINS}")
                        
                        # Refresh the button image to colored
                        display_name = t.replace("_", " ")
                        try:
                            raw_img = Image.open(f"img/buttons/{t}_btn.png").resize((130, 130))
                            win.images[f"btn_{t}"] = ImageTk.PhotoImage(raw_img)
                            bg_canvas.itemconfig(f"btn_{t}", image=win.images[f"btn_{t}"])
                        except:
                            bg_canvas.itemconfig(f"btn_{t}", fill="white") # Revert to normal color if it's text
            else:
                messagebox.showerror("Not enough coins", "You need 100 coins to unlock this theme!")

    def make_cmd(t):
        return lambda e: theme_click(t)

    # Pre-create all theme images/texts
    for theme_name in themes:
        display_name = theme_name.replace("_", " ")
        try:
            raw_img = Image.open(f"img/buttons/{theme_name}_btn.png").resize((130, 130))
            if theme_name not in config.UNLOCKED_THEMES:
                # Convert to greyscale for locked themes
                raw_img = raw_img.convert("L").convert("RGBA")
            win.images[f"btn_{theme_name}"] = ImageTk.PhotoImage(raw_img)
            btn_id = bg_canvas.create_image(0, 0, image=win.images[f"btn_{theme_name}"], tags=f"btn_{theme_name}")
        except:
            color = "white" if theme_name in config.UNLOCKED_THEMES else "gray"
            btn_id = bg_canvas.create_text(0, 0, text=display_name, font=("Arial", 14, "bold"), fill=color, tags=f"btn_{theme_name}")
            
        bg_canvas.tag_bind(btn_id, "<Button-1>", make_cmd(theme_name))
        bg_canvas.tag_bind(btn_id, "<Enter>", on_enter_cursor)
        bg_canvas.tag_bind(btn_id, "<Leave>", on_leave_cursor)

    def resize_canvas(event):
        if event.widget == bg_canvas:
            w, h = event.width, event.height
            if w < 100 or h < 100: return
            
            # Resize background
            if original_bg:
                resized_bg = original_bg.resize((w, h))
                win.images['bg'] = ImageTk.PhotoImage(resized_bg)
                bg_canvas.itemconfig("bg", image=win.images['bg'])
                
            # Resize title
            font_size = max(20, int(w * 0.05))
            bg_canvas.itemconfig("title", font=("Times New Roman", font_size, "bold"))
            
            # Resize back button
            btn_w = max(50, int(w * 0.12))
            btn_h = max(25, int(h * 0.08))
            if original_back:
                resized_back = original_back.resize((btn_w, btn_h))
                win.images['back'] = ImageTk.PhotoImage(resized_back)
                bg_canvas.itemconfig("back", image=win.images['back'])
            
            # Layout the grid
            btn_width = 120
            btn_height = 120
            cols = max(1, int((w - 40) // btn_width))
            
            grid_width = cols * btn_width
            start_x = (w - grid_width) / 2 + btn_width / 2
            start_y = h * 0.25 + btn_height / 2
            
            max_y = 0
            for i, theme_name in enumerate(themes):
                row = i // cols
                col = i % cols
                x = start_x + col * btn_width
                y = start_y + row * btn_height
                bg_canvas.coords(f"btn_{theme_name}", x, y)
                max_y = y + btn_height / 2
                
            # Configure scroll region
            bg_canvas.configure(scrollregion=(0, 0, w, max(h, max_y + 100)))
            update_fixed_elements()

    bg_canvas.bind("<Configure>", resize_canvas)
    
    # Bind scroll events to the whole window to ensure they work anywhere
    win.bind("<Enter>", lambda e: bg_canvas.bind_all("<MouseWheel>", _on_mousewheel))
    win.bind("<Leave>", lambda e: bg_canvas.unbind_all("<MouseWheel>"))
