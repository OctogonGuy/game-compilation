"""
Program: tic_tac_toe.py
Author: Alex Gill
A game for two players who take turns marking the spaces in
a three-by-three grid with X or O. The player who succeeds
in placing three of their marks in a horizontal, vertical,
or diagonal row is the winner.
"""
from tkinter import *
from tkinter import ttk
import random

# --- Global constants
EMPTY = 0       # Represents an empty item
ROWS = 3        # Number of rows
COLS = 3        # Number of columns
WIDTH = 375     # Width and height the board
PADDING = 30    # Padding around widgets

# --- Global variables ---
p1_marker = 'X'     # Player 1's marker
p2_marker = 'O'     # Player 2's marker
game_over = False   # Whether the game is over
cur_marker = None   # The current marker
spaces = None       # The grid of spaces
message = None      # The current message
play_button = None  # A button that starts the game over


def build_board(window):
    """
    Creates and displays the board on a window.
    Param window: The window on which to display the board
    """
    global spaces
    global message
    global play_button

    # Create the board and place it on the grid
    board = ttk.Frame(window, width=WIDTH, height=WIDTH)
    board.grid(row=0, column=0)
    board.grid_propagate(False)

    # Create a tile for each space and place them on the grid
    spaces = [[EMPTY for j in range(COLS)] for i in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            spaces[i][j] = ttk.Button(board, style='Grid_Standard.TButton',
                text=' ')
            spaces[i][j].grid(row=i, column=j, sticky=(N, S, E, W))
            spaces[i][j].bind('<ButtonPress>', place_marker)

    # Create a label for game messages
    message = StringVar(window)
    message_label = ttk.Label(window, style='Message.TLabel',
        textvariable=message)
    message_label.grid(row=1, column=0)

    # Create a button to play again
    play_button = ttk.Button(window, text='Play Again', style='Play.TButton')
    play_button.configure(command=play_again)
    play_button.state(['disabled'])
    play_button.grid(row=2, column=0)

    # Make the board resizable
    for i in range(ROWS):
        board.rowconfigure(i, weight=1)
    for i in range(COLS):
        board.columnconfigure(i, weight=1)


def marker_choice():
    """
    Randomly chooses the player to go first.
    """
    global cur_marker
    global message

    # Randomly decide whether x or o will go first
    if random.choice((True, False)):
        cur_marker = p1_marker
    else:
        cur_marker = p2_marker

    # Display this information to the user
    message.set(cur_marker + ' goes first.')


def place_marker(event):
    """
    Places the current marker on the calling event's
    location on the board. Then checks to see if a player
    has won or if the board is full and acts accordingly.
    Param event: The calling event
    """
    global game_over
    global cur_marker
    global message
    button = event.widget

    if not game_over:
        # Place the current marker in the space if empty
        if button['text'] == ' ':
            button['text'] = cur_marker
        else:
            message.set('That space is already occupied.')
            return

        # If the player won, alert the players and end the game
        if has_won(spaces, cur_marker):
            message.set(cur_marker + ' won!')
            game_over = True
            play_button.state(['!disabled'])

        # If the game is a tie, alert the players and end the game
        elif is_full(spaces):
            message.set('Tie game!')
            game_over = True
            play_button.state(['!disabled'])
        
        # Otherwise, it is the next player's turn
        else:
            if cur_marker == p1_marker:
                cur_marker = p2_marker
            else:
                cur_marker = p1_marker
            message.set(cur_marker + '\'s turn.')


def has_won(board, marker):
    """
    Checks to see if a player has won the game.
    Param board: The board to check
    Param marker: The marker to check for
    Return: True if the player has won; False otherwise
    """
    # Assume the player has not won
    won = False

    # Check each row for a win
    if board[0][0]['text'] == board[0][1]['text'] == board[0][2]['text'] == marker:
        highlight(board[0][0], board[0][1], board[0][2])
        won = True
    elif board[1][0]['text'] == board[1][1]['text'] == board[1][2]['text'] == marker:
        highlight(board[1][0], board[1][1], board[1][2])
        won = True
    elif board[2][0]['text'] == board[2][1]['text'] == board[2][2]['text'] == marker:
        highlight(board[2][0], board[2][1], board[2][2])
        won = True
    
    # Check each column for a win
    elif board[0][0]['text'] == board[1][0]['text'] == board[2][0]['text'] == marker:
        highlight(board[0][0], board[1][0], board[2][0])
        won = True
    elif board[0][1]['text'] == board[1][1]['text'] == board[2][1]['text'] == marker:
        highlight(board[0][1], board[1][1], board[2][1])
        won = True
    elif board[0][2]['text'] == board[1][2]['text'] == board[2][2]['text'] == marker:
        highlight(board[0][2], board[1][2], board[2][2])
        won = True
    
    # Check each diagonal for a win
    elif board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] == marker:
        highlight(board[0][0], board[1][1], board[2][2])
        won = True
    elif board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] == marker:
        highlight(board[0][2], board[1][1], board[2][0])
        won = True

    # Return won
    return won


def highlight(*buttons):
    """
    Highlights the text on the specified buttons.
    """
    # Apply the win style to the buttons
    for button in buttons:
        button.configure(style='Grid_Win.TButton')


def is_full(board):
    """
    Checks to see whether the board is full.
    Param board: The board to check
    Return: True if the board is full; False otherwise
    """
    # Assume the board is full
    full = True

    # Set full to false if any space is empty
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j]['text'] == ' ':
                full = False

    # Return full
    return full


def play_again():
    """
    Starts the game over again.
    """
    global game_over
    global play_button

    # Clear the spaces
    for i in range(ROWS):
        for j in range(COLS):
            spaces[i][j].configure(text=' ', style='Grid_Standard.TButton')

    # Choose who goes first
    marker_choice()

    # Set game_over to False
    game_over = False

    # Disable play_button
    play_button.state(['disabled'])


def set_window_resize(window):
    """Centers the window and prevents the it from shrinking past its
    default size."""
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + frm_width * 2
    height = window.winfo_height()
    tlb_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + tlb_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.minsize(width=width, height=height)


def main():
    # Create the root
    root = Tk()
    root.title('Tic-tac-toe')
    root.columnconfigure(0, weight=1, pad=PADDING)
    root.rowconfigure(0, weight=1)
    root.rowconfigure((0, 2), pad=PADDING)

    # Create styles for the buttons
    s = ttk.Style()
    s.configure('Grid_Standard.TButton', font=('Maiandra GD', 60),
        foreground='black')
    s.configure('Grid_Win.TButton', font=('Maiandra GD', 60),
        foreground='red')
    s.configure('Message.TLabel', font=('Arial', 12))
    s.configure('Play.TButton', font=('Calibri', 11))

    # Create and display the board
    build_board(root)
    
    # Set the window's resize properties
    set_window_resize(root)

    # Decide who goes first
    marker_choice()

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()