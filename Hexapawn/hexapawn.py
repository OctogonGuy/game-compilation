"""
File: hexapawn.py
Author: Alex Gill
Simulates the deterministic two-player game Hexapawn.
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from board import Board
from matchbox import Matchbox
import pathlib

# --- Global constants
FILENAME = 'matchboxes.txt'
HOW_TO_PLAY = 'how_to_play.txt'

# --- Global variables ---
selected_row = None         # The row of the selected pawn
selected_col = None         # The column of the selected pawn
board = None                # The board
matchboxes = None           # The matchboxes
move_num = 1                # The move number
turn = 'player_unselected'  # The state of the turn
last_matchbox = None        # The last matchbox that was drawn from
last_move = None            # The opponent's latest move
wins_losses = []            # List of player's wins and losses in order

def select(event):
    """Handles clicking on player pawn."""
    global turn; turn = 'player_selected'
    global selected_row; selected_row = event.widget.row
    global selected_col; selected_col = event.widget.col
    event.widget.master.configure(cursor='')
    go()


def deselect(event):
    """Handles clicking outside valid square."""
    global turn; turn = 'player_unselected'
    if event.widget.pawn == 'white':
        event.widget.master.configure(cursor='hand2')
    go()


def move(event):
    """Handles the player moving a pawn."""
    global selected_row
    global selected_col
    global board; board.pawn_move(selected_row, selected_col,
        event.widget.row, event.widget.col)
    event.widget.master.configure(cursor='')
    for row in board.squares:
        for square in row:
            square.bind('<Enter>', lambda e:
                square.master.configure(cursor=''))
            square.bind('<ButtonPress>', NONE)
    global turn; turn = 'opponent'
    check_winner('white')


def go():
    """Executes the appropriate action depending on the state of the
    board."""
    global selected_row
    global selected_col
    global move_num
    global turn
    global board
    global matchboxes
    global last_matchbox
    global last_move

    # Handle the player's turn when no pawn has been selected
    if turn == 'player_unselected':
        for row in board.squares:
            for square in row:
                if square.pawn == 'white':
                    square.bind('<Enter>', lambda e:
                        square.master.configure(cursor='hand2'))
                    square.bind('<ButtonPress>', select)
                else:
                    square.bind('<Enter>', lambda e:
                        square.master.configure(cursor=''))
                    square.bind('<ButtonPress>', None)
    
    # Handle the player's turn when a pawn has been selected
    elif turn == 'player_selected':
        for row in board.squares:
            for square in row:
                square.bind('<Enter>', lambda e:
                        square.master.configure(cursor=''))
                square.bind('<ButtonPress>', deselect)
        for square in board.squares[selected_row - 1]:
            if square.col == selected_col and square.pawn == None:
                square.bind('<Enter>', lambda e:
                        square.master.configure(cursor='hand2'))
                square.bind('<ButtonPress>', move)
            elif (square.col == selected_col - 1 \
                    or square.col == selected_col + 1) \
                    and square.pawn == 'black':
                square.bind('<Enter>', lambda e:
                        square.master.configure(cursor='hand2'))
                square.bind('<ButtonPress>', move)

    # Handle the opponent's turn
    elif turn == 'opponent':
        # Find the matchbox of the current board state
        found = False
        reverse = False
        for matchbox in matchboxes[move_num]:
            if board == matchbox.board_configuration:
                last_matchbox = matchbox
                found = True
                break
        if not found:
            for matchbox in matchboxes[move_num]:
                if board == matchbox.board_configuration.reverse():
                    last_matchbox = matchbox
                    found = True
                    reverse = True
                    break
        
        # Move according to what bead falls out of the matchbox
        last_move = last_matchbox.get_bead()
        if reverse:
            board.pawn_move(last_move[0], 2 - last_move[1],
                            last_move[2], 2- last_move[3])
        else:
            board.pawn_move(last_move[0], last_move[1],
                            last_move[2], last_move[3])

        # Player's turn
        turn = 'player_unselected'

        # Check to see if opponent won
        check_winner('black')


def check_winner(pawn):
    """
    Looks for a winner.
    Param: pawn The color of the player in question.
    """
    global board
    global turn
    global move_num
    global matchboxes
    global last_matchbox
    global last_move
    global wins_losses
    found = False
    valid_moves = False
    player_won = False
    opponent_won = False

    # Check to see if the player has won
    if pawn == 'white':
        for square in board.squares[0]:
            if square.pawn == 'white':
                player_won = True
                break
        # Check to see if the player has won by default
        if not player_won:
            for row_num in range(len(board.squares)):
                for square in board.squares[row_num]:
                    if square.pawn == 'white':
                        for suc_square in board.squares[row_num - 1]:
                            if square.col == suc_square.col \
                                    and suc_square.pawn == None:
                                valid_moves = True
                            elif (square.col == suc_square.col - 1 \
                                    or square.col == suc_square.col + 1) \
                                    and suc_square.pawn == 'black':
                                valid_moves = True
                    elif square.pawn == 'black':
                        found = True
            if not found or not valid_moves:
                player_won = True
        
    # Check to see if the opponent has won
    elif pawn == 'black':
        for square in board.squares[2]:
            if square.pawn == 'black':
                opponent_won = True
                break
        # Check to see if the opponent has won by default
        if not opponent_won:
            for row_num in range(len(board.squares)):
                for square in board.squares[row_num]:
                    if square.pawn == 'black':
                        for suc_square in board.squares[row_num + 1]:
                            if square.col == suc_square.col \
                                    and suc_square.pawn == None:
                                valid_moves = True
                            elif (square.col == suc_square.col - 1 \
                                    or square.col == suc_square.col + 1) \
                                    and suc_square.pawn == 'white':
                                valid_moves = True
                    elif square.pawn == 'white':
                        found = True
            if not found or not valid_moves:
                opponent_won = True
    
    # Player won
    if player_won:
        display_winner('You won', 900)
        last_matchbox.remove_bead(last_move)
        wins_losses.append('W')
    
    # Opponent won
    elif opponent_won:
        display_winner('Opponent won', 900)
        wins_losses.append('L')

    # Reset the game if either player won
    if player_won or opponent_won:
        move_num = 1
        turn = 'player_unselected'
        board.master.after(1000, lambda: board.reset())
        board.master.after(1100, lambda: go())
    else:
        move_num += 1
        if turn == 'opponent':
            board.master.after(1000, lambda: go())
        else:
            go()


def display_winner(message, interval):
    """Displays the winner message and hides it after an interval."""
    winner_label = ttk.Label(board.master, text=message, style='winner.TLabel')
    winner_label.grid(row=0, column=0)
    board.master.after(interval, lambda: winner_label.grid_forget())


def read_matchboxes(filename):
    """Reads a list of matchboxes from a file."""
    # Instantiate matchboxes
    global matchboxes; matchboxes = {2:[], 4:[], 6:[]}

    # Open the file
    path = str(pathlib.Path(__file__).parent.resolve()) + '\\' + filename
    file = open(path)
    file.readline()

    # Perform a priming read
    move_num = file.readline().strip()

    # Read the rest of the lines from the file
    while move_num != '':
        # Convert the move number to an integer
        move_num = int(move_num)
        # Read the pawn configuration
        pawns = file.readline().strip().split()
        # Read the possible moves
        moves = file.readline().strip().split(',')
        possible_moves = []
        for move in moves:
            cur_move = move.split()
            for i in range(len(cur_move)):
                cur_move[i] = int(cur_move[i])
            possible_moves.append(tuple(cur_move))
        # Instantiate the matchbox
        matchboxes[move_num].append(Matchbox(move_num, Board(None, pawns),
            possible_moves))
        # Attempt to read the next move number
        file.readline()
        move_num = file.readline().strip()

    # Close the file
    file.close()


def set_window_resize(window):
    """Centers the window and prevents it from being shrunken past its
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


def show_how_to_play(root):
    """Opens a window showing the instructions for how to play."""
    # Create the window
    window = Toplevel(root)
    window.title('How to Play')
    window.configure(padx=2, pady=2)
    window.resizable(False, False)

    # Read the instructions from a text file into a string
    inputfile = open(str(pathlib.Path(__file__).parent.resolve()) + \
        '\\' + HOW_TO_PLAY, 'r')
    instructions_text = inputfile.read()
    inputfile.close()

    # Create text for the instructions
    instructions = Text(window, width=50, height=20, wrap=WORD,
        font=('Times', 12))
    instructions.insert(0.0, instructions_text)
    instructions['state'] = DISABLED
    instructions.grid(row=0, column=0, sticky=(N, S, E, W))

    # Create a scrollbar for the instructions
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=
        instructions.yview)
    scrollbar.grid(column=1, row=0, sticky=(N, S))
    instructions['yscrollcommand'] = scrollbar.set

    # Create a button to exit
    ok_button = ttk.Button(window, text='OK', command=window.destroy)
    ok_button.grid(row=1, column=0, columnspan=2)

    # Set the window's resize property
    set_window_resize(window)


def confirm_exit_dialog(root):
    """Shows a confirmation dialog to the user before exiting."""
    quit = messagebox.askyesno('Warning',
                               'Are you sure you want to quit?' +
                               '\nYou will lose all your progress.')
    if quit:
        show_results_dialog(root)


def show_results_dialog(root):
    """Shows the wins and losses and quits upon action."""
    global wins_losses
    wl = ''
    for i in range(len(wins_losses)):
        wl += wins_losses[i] + ' '
        if i % 25 == 24:
            wl +='\n'
    messagebox.showinfo('Results',
                        'Here are your wins and losses against the ' + \
                            'computer in order:\n' +
                        wl)
    root.destroy()
    

def main():
    # Create the root
    root = Tk()
    root.title('Hexapawn')
    root.protocol('WM_DELETE_WINDOW', lambda: confirm_exit_dialog(root))

    # Create styles
    s = ttk.Style()
    s.configure('winner.TLabel', font=('Calibri', 24), foreground='red')

    # Read the matchboxes
    read_matchboxes(FILENAME)

    # Create a menu bar
    root.option_add('*tearOff', FALSE)
    menubar = Menu(root)
    root['menu'] = menubar
    menu_game = Menu(menubar)
    menu_help = Menu(menubar)
    menubar.add_cascade(menu=menu_game, label='Game')
    menubar.add_cascade(menu=menu_help, label='Help')
    menu_game.add_command(label='Exit', command=lambda:
        confirm_exit_dialog(root))
    menu_help.add_command(label='How to play', command=lambda:
        show_how_to_play(root))

    # Create the board and display it
    global board; board = Board(root)
    board.grid(row=0, column=0)

    # Start the game
    go()
    
    # Set the root's resize property
    set_window_resize(root)
    
    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()