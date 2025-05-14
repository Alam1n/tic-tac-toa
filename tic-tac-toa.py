import matplotlib.pyplot as plt
import numpy as np
import random

# Initialize the board (3x3 empty)
board = np.full((3, 3), '', dtype=str)

# Current player: 'X' starts
current_player = ['X']

# Create the plot
fig, ax = plt.subplots()
ax.set_xticks([0, 1, 2])
ax.set_yticks([0, 1, 2])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(True)
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 2.5)
plt.gca().invert_yaxis()

# Draw X and O
def draw_symbol(x, y, symbol):
    if symbol == 'X':
        ax.plot([x-0.3, x+0.3], [y-0.3, y+0.3], color='blue', lw=2)
        ax.plot([x-0.3, x+0.3], [y+0.3, y-0.3], color='blue', lw=2)
    elif symbol == 'O':
        circle = plt.Circle((x, y), 0.3, color='red', fill=False, lw=2)
        ax.add_patch(circle)

# Check for win or draw
def check_winner():
    for i in range(3):
        if all(board[i, :] == board[i, 0]) and board[i, 0] != '':
            return board[i, 0]
        if all(board[:, i] == board[0, i]) and board[0, i] != '':
            return board[0, i]
    if all([board[i, i] == board[0, 0] and board[i, i] != '' for i in range(3)]):
        return board[0, 0]
    if all([board[i, 2 - i] == board[0, 2] and board[i, 2 - i] != '' for i in range(3)]):
        return board[0, 2]
    if np.all(board != ''):
        return 'Draw'
    return None

def on_click(event):
    if event.inaxes != ax:
        return

    col, row = int(round(event.xdata)), int(round(event.ydata))
    
    if 0 <= row < 3 and 0 <= col < 3 and board[row, col] == '':
        # Player move
        board[row, col] = current_player[0]
        draw_symbol(col, row, current_player[0])
        winner = check_winner()
        if winner:
            print(f"{winner} wins!" if winner != 'Draw' else "It's a draw!")
            fig.canvas.mpl_disconnect(cid)
            plt.draw()
            return

        plt.draw()

        # Switch to AI
        current_player[0] = 'O' if current_player[0] == 'X' else 'X'
        ai_r, ai_c = ai_move(current_player[0])
        board[ai_r, ai_c] = current_player[0]
        draw_symbol(ai_c, ai_r, current_player[0])
        winner = check_winner()
        if winner:
            print(f"{winner} wins!" if winner != 'Draw' else "It's a draw!")
            fig.canvas.mpl_disconnect(cid)

        # Back to player
        current_player[0] = 'O' if current_player[0] == 'X' else 'X'
        plt.draw()


def ai_move(symbol):
    opponent = 'X' if symbol == 'O' else 'O'

    # 1. Try to win (Attack)
    for i in range(3):
        # Check rows
        row = board[i, :]
        if list(row).count(symbol) == 2 and list(row).count('') == 1:
            col = list(row).index('')
            return i, col
        # Check columns
        col = board[:, i]
        if list(col).count(symbol) == 2 and list(col).count('') == 1:
            row_i = list(col).index('')
            return row_i, i

    # Check diagonals
    diag1 = [board[i, i] for i in range(3)]
    if diag1.count(symbol) == 2 and diag1.count('') == 1:
        i = diag1.index('')
        return i, i
    diag2 = [board[i, 2 - i] for i in range(3)]
    if diag2.count(symbol) == 2 and diag2.count('') == 1:
        i = diag2.index('')
        return i, 2 - i

    # 2. Try to block (Defend)
    for i in range(3):
        # Check rows
        row = board[i, :]
        if list(row).count(opponent) == 2 and list(row).count('') == 1:
            col = list(row).index('')
            return i, col
        # Check columns
        col = board[:, i]
        if list(col).count(opponent) == 2 and list(col).count('') == 1:
            row_i = list(col).index('')
            return row_i, i

    # Check diagonals
    if diag1.count(opponent) == 2 and diag1.count('') == 1:
        i = diag1.index('')
        return i, i
    if diag2.count(opponent) == 2 and diag2.count('') == 1:
        i = diag2.index('')
        return i, 2 - i

    # 3. Neutral move - pick random empty cell
    empty = [(r, c) for r in range(3) for c in range(3) if board[r, c] == '']
    return random.choice(empty) if empty else None


# Connect click event
cid = fig.canvas.mpl_connect('button_press_event', on_click)

plt.title("Tic Tac Toe with Matplotlib")
plt.show()
