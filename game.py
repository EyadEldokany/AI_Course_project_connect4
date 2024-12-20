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
AI_DEPTH = 0  # Limit Minimax depth for performance

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

def evaluate_board(board):
    """Evaluate the board for AI advantage."""
    score = 0

    # Score center column higher as it allows more winning possibilities
    center_column = [board[row][COLUMNS // 2] for row in range(ROWS)]
    center_count = center_column.count("O")
    score += center_count * 3

    # Check all rows for potential
    for row in range(ROWS):
        row_array = board[row]
        for col in range(COLUMNS - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, "O")
            score -= evaluate_window(window, "X")

    # Check all columns for potential
    for col in range(COLUMNS):
        col_array = [board[row][col] for row in range(ROWS)]
        for row in range(ROWS - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, "O")
            score -= evaluate_window(window, "X")

    # Check all positive diagonals for potential
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, "O")
            score -= evaluate_window(window, "X")

    # Check all negative diagonals for potential
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, "O")
            score -= evaluate_window(window, "X")

    return score

def evaluate_window(window, piece):
    """Evaluate a window of four cells."""
    score = 0
    opp_piece = "X" if piece == "O" else "O"

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(" ") == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(" ") == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(" ") == 1:
        score -= 80  # Block opponent's winning moves aggressively

    return score

def minimax(board, depth, maximizing_player):
        # Get all valid columns where a piece can be dropped
    valid_columns = get_valid_columns(board)

    # Base case: Check if the game is over (win, loss, or draw) or depth limit reached
    if check_win(board, "O"):  # If AI (O) wins, return a very high score
        return (None, float("inf"))
    if check_win(board, "X"):  # If player (X) wins, return a very low score
        return (None, -float("inf"))
    if is_draw(board) or depth == 0:  # If it's a draw or depth is 0, evaluate the board
        return (None, evaluate_board(board))

    # Recursive case: Explore the game tree
    if maximizing_player:  # AI's turn (maximize score)
        value = -float("inf")  # Start with the worst possible score
        best_column = random.choice(valid_columns)  # Pick a random valid column initially

        # Iterate through all valid columns
        for column in valid_columns:
            # Simulate dropping a piece in the column
            temp_board = copy.deepcopy(board)
            drop_piece_in_simulation(temp_board, column, "O")

            # Recursively call minimax for the opponent's turn (minimizing player)
            new_score = minimax(temp_board, depth - 1, False)[1]

            # Update the best score and column if a better score is found
            if new_score > value:
                value = new_score
                best_column = column

        return best_column, value
    else:  # Opponent's turn (minimize score)
        value = float("inf")  # Start with the best possible score for minimizing
        best_column = random.choice(valid_columns)  # Pick a random valid column initially

        # Iterate through all valid columns
        for column in valid_columns:
            # Simulate dropping a piece in the column
            temp_board = copy.deepcopy(board)
            drop_piece_in_simulation(temp_board, column, "X")

            # Recursively call minimax for the AI's turn (maximizing player)
            new_score = minimax(temp_board, depth - 1, True)[1]

            # Update the best score and column if a worse score is found
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

def choose_mode(mode):
    global player_vs_ai
    player_vs_ai = (mode == "AI")
    menu_frame.pack_forget()
    if player_vs_ai:
        difficulty_frame.pack()  # Show the difficulty selection screen
    else:
        game_frame.pack()
        reset_game()

def choose_difficulty(difficulty):
    global AI_DEPTH
    if difficulty == "Easy":
        AI_DEPTH = 1
    elif difficulty == "Normal":
        AI_DEPTH = 3
    elif difficulty == "Advanced":
        AI_DEPTH = 4
    difficulty_frame.pack_forget()
    game_frame.pack()
    reset_game()

# Initialize the game
board = create_board()
# GUI SECTION
# Create the GUI
root = tk.Tk()
root.title("Connect 4")
root.configure(bg="#f0f0f0")

# Menu Frame
menu_frame = tk.Frame(root, bg="#f0f0f0")
menu_frame.pack()
# Button for Player vs AI mode
# When clicked, it calls choose_mode("AI") and navigates to the difficulty selection screen.
tk.Label(menu_frame, text="Choose Game Mode", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)
tk.Button(menu_frame, text="Player vs Player", font=("Arial", 16),
            command=lambda: choose_mode("PvP"), bg="lightgreen", width=20).pack(pady=5)
tk.Button(menu_frame, text="Player vs AI", font=("Arial", 16),
            command=lambda: choose_mode("AI"), bg="lightblue", width=20).pack(pady=5)

# Difficulty Frame
difficulty_frame = tk.Frame(root, bg="#f0f0f0")
# Add a label for difficulty selection
tk.Label(difficulty_frame, text="Select Difficulty", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)
# Button for Easy difficulty
tk.Button(difficulty_frame, text="Easy", font=("Arial", 16),
            command=lambda: choose_difficulty("Easy"), bg="lightgreen", width=20).pack(pady=5)
# Button for Normal difficulty
tk.Button(difficulty_frame, text="Normal", font=("Arial", 16),
            command=lambda: choose_difficulty("Normal"), bg="blue", width=20).pack(pady=5)
# Button for Advanced difficulty
tk.Button(difficulty_frame, text="Advanced", font=("Arial", 16),
            command=lambda: choose_difficulty("Advanced"), bg="red", width=20).pack(pady=5)

# Game Frame
game_frame = tk.Frame(root, bg="#f0f0f0") # Create the frame for the game board

# Canvas for drawing the Connect 4 board
# Each circle represents a slot on the board. It responds to mouse clicks to drop pieces
canvas = tk.Canvas(game_frame, width=COLUMNS * 100, height=ROWS * 100, bg="blue")
canvas.pack()
canvas.bind("<Button-1>", handle_click)

# Draw the initial empty board
draw_board()
# Label for showing the current scores of both players
score_label = tk.Label(game_frame, text=f"Player X: 0  |  Player O: 0", font=("Arial", 16), bg="#f0f0f0")
score_label.pack(pady=10) # Add some padding for better spacing

# This button allows the user to reset the game at any time. It calls the reset_game() function.
restart_button = tk.Button(game_frame, text="Restart Game", font=("Arial", 16), command=reset_game, bg="orange")
restart_button.pack(pady=10)
switch_button = tk.Button(game_frame, text="Switch Mode", font=("Arial", 14), command=switch, bg="orange")
switch_button.pack(pady=10)

root.mainloop()
