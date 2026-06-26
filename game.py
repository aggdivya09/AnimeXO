from tkinter import *
from PIL import Image, ImageTk
import config
import math
import random

def start_game(root, mode):
    win = Frame(root)
    win.place(x=0, y=0, relwidth=1, relheight=1)

    theme = config.CURRENT_THEME
    
    bg_canvas = Canvas(win, highlightthickness=0)
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

    try:
        original_bg = Image.open(f"img/BG/{theme}_bg.png")
    except:
        try:
            original_bg = Image.open("bg.png")
        except:
            original_bg = None

    win.images = {}

    def resize_bg(event):
        if event.widget == bg_canvas:
            new_w, new_h = event.width, event.height
            if new_w > 100 and new_h > 100 and original_bg:
                bg_canvas.delete("bg")
                resized_bg = original_bg.resize((new_w, new_h))
                win.images['bg'] = ImageTk.PhotoImage(resized_bg)
                bg_canvas.create_image(0, 0, image=win.images['bg'], anchor="nw", tags="bg")
                bg_canvas.tag_lower("bg")

    bg_canvas.bind("<Configure>", resize_bg)

    # Load X and O images
    try:
        x_img_raw = Image.open(f"img/X_O/{theme}/X_sym.png").resize((90, 90))
        win.images['X'] = ImageTk.PhotoImage(x_img_raw)
    except:
        win.images['X'] = None

    try:
        o_img_raw = Image.open(f"img/X_O/{theme}/O_sym.png").resize((90, 90))
        win.images['O'] = ImageTk.PhotoImage(o_img_raw)
    except:
        win.images['O'] = None

    # Game State
    board = [' ' for _ in range(9)]
    current_player = 'X'
    game_active = True

    # UI Elements
    board_frame = Frame(win, bg="#333333", bd=5)
    # Using relwidth=0.4 and relheight=0.7 keeps it perfectly square on a 16:9 aspect ratio window
    board_frame.place(relx=0.5, rely=0.70, anchor="center", relwidth=0.32, relheight=0.5)

    buttons = []

    def check_winner(b):
        lines = [
            (0,1,2), (3,4,5), (6,7,8), # rows
            (0,3,6), (1,4,7), (2,5,8), # cols
            (0,4,8), (2,4,6)           # diagonals
        ]
        for line in lines:
            if b[line[0]] == b[line[1]] == b[line[2]] != ' ':
                return b[line[0]]
        if ' ' not in b:
            return 'Draw'
        return None

    def minimax(b, depth, is_maximizing):
        winner = check_winner(b)
        if winner == 'O': return 10 - depth
        if winner == 'X': return depth - 10
        if winner == 'Draw': return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'O'
                    score = minimax(b, depth + 1, False)
                    b[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'X'
                    score = minimax(b, depth + 1, True)
                    b[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def ai_move():
        nonlocal current_player
        
        available_moves = [i for i in range(9) if board[i] == ' ']
        if not available_moves: return
        
        # 30% chance to pick a random move instead of optimal minimax
        if random.random() < 0.3:
            best_move = random.choice(available_moves)
        else:
            best_score = -math.inf
            best_move = -1
            for i in available_moves:
                board[i] = 'O'
                score = minimax(board, 0, False)
                board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        
        if best_move != -1:
            make_move(best_move)

    def handle_click(index):
        if not game_active or board[index] != ' ':
            return
            
        make_move(index)

        # AI Turn
        if game_active and mode == "single" and current_player == 'O':
            win.after(300, ai_move)

    def make_move(index):
        nonlocal current_player, game_active
        board[index] = current_player
        
        if win.images.get(current_player):
            buttons[index].config(image=win.images[current_player], text='')
        else:
            color = "#c22c3e" if current_player == 'X' else "#2c6ac2"
            buttons[index].config(text=current_player, fg=color, image='')
        
        winner = check_winner(board)
        if winner:
            game_active = False
            show_game_over(winner)
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            # If playing single player, the text shows human vs AI
            if mode == "single" and current_player == 'O':
                turn_label.config(text="AI is thinking...", fg="#2c6ac2")
            else:
                turn_label.config(text=f"Player {current_player}'s Turn", fg="#c22c3e" if current_player == 'X' else "#2c6ac2")

    def show_game_over(winner):
        msg = f"Player {winner} Wins!" if winner != 'Draw' else "It's a Draw!"
        
        if winner == 'X':
            config.COINS += 20
            config.save_state()
            msg += "\n+20 Coins!"

        turn_label.config(text=msg, fg="white")
        
        overlay = Frame(win, bg="black")
        overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.6)
        
        Label(overlay, text=msg, font=("Times New Roman", 24, "bold"), bg="black", fg="white").pack(pady=20)
        
        Button(overlay, text="Play Again", font=("Arial", 16, "bold"), bg="#c22c3e", fg="white", 
               cursor="hand2", command=lambda: [overlay.destroy(), reset_game()]).pack(pady=10)
        
        Button(overlay, text="Back to Menu", font=("Arial", 16, "bold"), bg="#333333", fg="white", 
               cursor="hand2", command=go_back).pack(pady=10)

    def reset_game():
        nonlocal board, current_player, game_active
        board = [' ' for _ in range(9)]
        current_player = 'X'
        game_active = True
        turn_label.config(text="Player X's Turn", fg="#c22c3e")
        for btn in buttons:
            btn.config(text=' ', image='')

    def go_back():
        win.destroy()

    board_frame.grid_propagate(False)

    # Draw grid
    for i in range(3):
        board_frame.columnconfigure(i, weight=1, uniform="col")
        board_frame.rowconfigure(i, weight=1, uniform="row")
        for j in range(3):
            index = i * 3 + j
            btn = Button(board_frame, text=' ', font=("Arial", 60, "bold"), bg="white", 
                         activebackground="#f0f0f0", cursor="hand2",
                         command=lambda idx=index: handle_click(idx))
            btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
            buttons.append(btn)

    # Top info label
    turn_label = Label(win, text="Player X's Turn", font=("Times New Roman", 25, "bold"), fg="#c22c3e", bg="black")
    turn_label.place(relx=0.5, rely=0.05, anchor="center")

    # Back button
    try:
        back_btn_img = ImageTk.PhotoImage(Image.open("img/menu_buttons/back.png").resize((100, 50)))
        back_btn = Label(win, image=back_btn_img, cursor="hand2", bg="black")
        back_btn.image = back_btn_img
        back_btn.place(x=30, y=30)
        back_btn.bind("<Button-1>", lambda e: go_back())
    except:
        back_btn = Button(win, text="← BACK", font=("Arial", 14, "bold"), fg="white", bg="black", command=go_back)
        back_btn.place(x=30, y=30)
