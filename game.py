import tkinter as tk
from tkinter import messagebox
import random
import copy

ROWS = 6
COLUMNS = 7

# Initialize global variables
current_player = "X"
board = []
player_vs_ai = False
scores = {"X": 0, "O": 0}
AI_DEPTH = 3  # Limit Minimax depth for performance

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def check_win(board, piece):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == piece:
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == piece:
                return True

    # Check diagonals (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == piece:
                return True

    # Check diagonals (negative slope)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == piece:
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_valid_columns(board):
    return [col for col in range(COLUMNS) if board[0][col] == " "]

def drop_piece_in_simulation(board, column, piece):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = piece
            return True
    return False

def minimax(board, depth, maximizing_player):
    if check_win(board, "O"):
        return (None, 100000)
    if check_win(board, "X"):
        return (None, -100000)
    if is_draw(board) or depth == 0:
        return (None, 0)

    valid_columns = get_valid_columns(board)
    if maximizing_player:
        value = -float("inf")
        best_column = random.choice(valid_columns)
        for column in valid_columns:
            temp_board = copy.deepcopy(board)
            drop_piece_in_simulation(temp_board, column, "O")
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                best_column = column
        return best_column, value
    else:
        value = float("inf")
        best_column = random.choice(valid_columns)
        for column in valid_columns:
            temp_board = copy.deepcopy(board)
            drop_piece_in_simulation(temp_board, column, "X")
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                best_column = column
        return best_column, value

def ai_move():
    global board, current_player
    col, _ = minimax(board, AI_DEPTH, True)
    drop_piece(col)

def drop_piece(column):
    global current_player, board

    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = current_player
            draw_piece(row, column, "red" if current_player == "X" else "yellow")
            if check_win(board, current_player):
                scores[current_player] += 1
                update_scores()
                messagebox.showinfo("Game Over", f"Player {current_player} wins!")
                reset_game()
                return
            elif is_draw(board):
                messagebox.showinfo("Game Over", "It's a draw!")
                reset_game()
                return
            else:
                current_player = "O" if current_player == "X" else "X"
                if player_vs_ai and current_player == "O":
                    root.after(500, ai_move)
            return
    messagebox.showwarning("Invalid Move", "Column is full!")

def reset_game():
    global board, current_player
    board = create_board()
    current_player = "X"
    canvas.delete("all")
    draw_board()
def switch():
    game_frame.pack_forget()
    menu_frame.pack()   
    #function for button 
def update_scores():
    score_label.config(text=f"Player X: {scores['X']}  |  Player O: {scores['O']}")

def choose_mode(mode):
    global player_vs_ai
    player_vs_ai = (mode == "AI")
    menu_frame.pack_forget()
    game_frame.pack()
    reset_game()

def draw_board():
    # Draw the grid and empty slots
    for row in range(ROWS):
        for col in range(COLUMNS):
            x1, y1 = 10 + col * 100, 10 + row * 100
            x2, y2 = 90 + col * 100, 90 + row * 100
            canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")

def draw_piece(row, column, color):
    # Draw a piece in the specified slot
    x1, y1 = 10 + column * 100, 10 + row * 100
    x2, y2 = 90 + column * 100, 90 + row * 100
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")

def handle_click(event):
    # Get the column based on the x-coordinate of the click
    x = event.x
    column = x // 100
    if column >= 0 and column < COLUMNS:
        drop_piece(column)

# Initialize the game
board = create_board()

# Create the GUI
root = tk.Tk()
root.title("Connect 4")
root.configure(bg="#f0f0f0")

# Menu Frame
menu_frame = tk.Frame(root, bg="#f0f0f0")
menu_frame.pack()

tk.Label(menu_frame, text="Choose Game Mode", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)
tk.Button(menu_frame, text="Player vs Player", font=("Arial", 16),
          command=lambda: choose_mode("PvP"), bg="lightgreen", width=20).pack(pady=5)
tk.Button(menu_frame, text="Player vs AI", font=("Arial", 16),
          command=lambda: choose_mode("AI"), bg="lightblue", width=20).pack(pady=5)

# Game Frame
game_frame = tk.Frame(root, bg="#f0f0f0")

canvas = tk.Canvas(game_frame, width=COLUMNS * 100, height=ROWS * 100, bg="blue")
canvas.pack()
canvas.bind("<Button-1>", handle_click)

draw_board()

score_label = tk.Label(game_frame, text=f"Player X: 0  |  Player O: 0", font=("Arial", 16), bg="#f0f0f0")
score_label.pack(pady=10)

restart_button = tk.Button(game_frame, text="Restart Game", font=("Arial", 16), command=reset_game, bg="orange")
restart_button.pack(pady=10)
restart_button = tk.Button(game_frame, text="Switch Mode", font=("Arial", 14), command=switch, bg="orange")
restart_button.pack(pady=10)      #button of returning to modes

root.mainloop()
