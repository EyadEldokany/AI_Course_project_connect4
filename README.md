# Connect 4 Game with AI and GUI

This project is a Python implementation of the classic Connect 4 game with a graphical user interface (GUI) built using the `tkinter` library. It supports two game modes: Player vs Player (PvP) and Player vs AI (PvAI). The AI opponent uses the Minimax algorithm with adjustable difficulty levels.

---

## Features

### Game Modes
- **Player vs Player (PvP):** Two human players can take turns to play the game.
- **Player vs AI (PvAI):** Play against an AI opponent. The AI difficulty can be adjusted to Easy, Normal, or Advanced.

### AI Logic
- AI is implemented using the **Minimax algorithm** with a depth limit for performance.
- AI evaluates board states using a heuristic function to make optimal moves.

### GUI
- Interactive game board implemented using `tkinter.Canvas`.
- Players can drop pieces by clicking on the column of their choice.
- Visual feedback for game progress with colored pieces (red for Player X and yellow for Player O).
- Displays scores for both players.
- Buttons for restarting the game and switching between game modes.

---

## Requirements

- Python 3.x

---

## How to Run

1. Clone or download the repository.
2. Ensure you have Python 3 installed.
3. Run the following command in your terminal or IDE:
   ```bash
   python connect4.py
   ```
4. The game window will open. Choose the desired game mode from the menu and start playing!

---

## Game Rules

1. Players take turns to drop their pieces into one of the 7 columns.
2. A player wins by forming a horizontal, vertical, or diagonal line of 4 consecutive pieces.
3. If the board fills up without a winner, the game ends in a draw.

---

## Files

- **`connect4.py`**: Contains the game logic, AI implementation, and GUI.
- **`README.md`**: This file, providing an overview of the project.

---

## Code Overview

### Main Components

1. **Game Logic**:
   - `create_board`: Initializes the game board.
   - `check_win`: Checks for winning conditions.
   - `is_draw`: Determines if the game is a draw.

2. **AI Logic**:
   - `minimax`: Implements the Minimax algorithm with depth control for AI moves.
   - `evaluate_board`: Evaluates the board state using a scoring heuristic.
   - `drop_piece_in_simulation`: Simulates moves for AI evaluation.

3. **GUI**:
   - `draw_board`: Draws the initial game board.
   - `draw_piece`: Updates the board with player pieces.
   - `handle_click`: Handles player input via mouse clicks.

4. **Game Modes**:
   - `choose_mode`: Allows switching between PvP and PvAI.
   - `choose_difficulty`: Sets AI difficulty level.

5. **Utilities**:
   - `reset_game`: Resets the game board and state.
   - `update_scores`: Updates the score display.

---

## Difficulty level

- Easy: Depth = 1
- Normal: Depth = 3
- Advanced: Depth = 4

---

## Acknowledgments

This project was created as an educational exercise to practice Python programming, game logic, and GUI design.

---

## License

This project is licensed under the MIT License. Feel free to use and modify it as you like.

