"""
Program: mastermind.py
Author: Alex Gill
Allows the user to play a game of Mastermind.
"""
from tkinter import *
from tkinter import ttk
from button import MButton
from peg import MPeg
import random
import pathlib

# --- Global constants ---
PEG_SPACING = 5         # The spacing between pegs on the grid
V_SPACING = 15          # The vertical spacing between widgets
H_SPACING = 10          # The horizontal spacing between widgets
PADDING = 20            # The padding around the edge of the screen
CODE_DIAMETER = 50      # The diameter of the code pegs and holes
KEY_DIAMETER = 20       # The diameter of the key pegs and holes
BUTTON_DIAMETER = 50    # The diameter of the buttons
COLORS = ('red', 'blue', 'green', 'yellow', # The peg colors
         'purple', 'orange', 'cyan', 'magenta')
HOLE_COLOR = 'gray'     # The color of the holes
HIDDEN_COLOR = 'lightgray'      # The color of the hidden row
HIT_COLOR = 'black'     # The color of the 'hit' key peg
BLOW_COLOR = 'white'    # The color of the 'blow' key peg
FILENAME = 'how_to_play.txt'    # The file name of the instructions text

# --- Global variables ---
num_rows = 6                # The number of rows / guesses the player can make
num_holes = 4               # The number of holes / pegs per row
num_colors = 6              # The number of colors that can be in the pattern
repeating_colors = False    # Whether to repeat colors
cur_row = 0                 # The row the player is on
cur_hole = 0                # The hole the player is on
game_over = False           # Indicates if the game is finished

# --- GUI components ---
message = None          # String variable message to display as message
footer_text = None      # A string variable message to display in the footer.
code_grid = None        # The grid of code pegs
key_grid = None         # The grid of key pegs
hidden_row = None       # The hidden row of pegs
hidden_pattern = None   # The hidden pattern
back_button = None      # Back button
confirm_button = None   # Confirm button


def build_board(window):
    """Builds the board."""
    global code_grid
    global key_grid
    global hidden_row
    global hidden_pattern
    global back_button
    global confirm_button

    # Reset the current row and hole and game over status
    global cur_row; cur_row = 0
    global cur_hole; cur_hole = 0
    global game_over; game_over = False

    # Remove all widgets in the window, if there are any
    for widget in window.winfo_children():
        widget.grid_remove()

    # Create the message label
    global message; message = StringVar(window)
    message_label = ttk.Label(window, textvariable=message,
        style='message.TLabel')
    message_label.grid(row=0, column=0, pady=(0, V_SPACING))

    # Set the text of the footer label
    footer_text.set('Repeating colors: ' + \
                    ('Yes' if repeating_colors else 'No') + \
                    '\tSlots: ' + str(num_holes) + \
                    '\tColors: ' + str(num_colors))

    # Create a grid of holes for code pegs
    code_frame = ttk.Frame(window)
    code_frame.grid(row=1, column=0, pady=(0, V_SPACING))
    code_grid = [[MPeg(code_frame, CODE_DIAMETER, HOLE_COLOR)
                for j in range(num_holes)] for i in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_holes):
            code_grid[i][j].grid(row=i, column=j)
            if i < num_rows - 1:
                code_grid[i][j].grid_configure(pady=(0, PEG_SPACING))
            if j < num_holes - 1:
                code_grid[i][j].grid_configure(padx=(0, PEG_SPACING))
            else:
                code_grid[i][j].grid_configure(padx=(0, H_SPACING))
    
    # Create a grid of holes for key pegs adjacent to the code grid
    key_grid = [[MPeg(code_frame, KEY_DIAMETER, HOLE_COLOR)
                for j in range(num_holes)] for i in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_holes):
            key_grid[i][j].grid(row=i, column=num_holes+j)
            if i < num_rows - 1:
                key_grid[i][j].grid_configure(pady=(0, PEG_SPACING))
            if j < num_holes - 1:
                key_grid[i][j].grid_configure(padx=(0, PEG_SPACING))

    # Create a row for the hidden pattern
    pattern_frame = ttk.Frame(window, style='hidden.TFrame')
    pattern_frame.grid(row=2, column=0, pady=(0, V_SPACING))
    colors = list(COLORS[0:num_colors])
    hidden_row = [MPeg(pattern_frame, CODE_DIAMETER, HIDDEN_COLOR)
                    for i in range(num_holes)]
    if repeating_colors:
        hidden_pattern = [MPeg(pattern_frame, CODE_DIAMETER,
                            random.choice(colors)) for i in range(num_holes)]
    else:
        hidden_pattern = [MPeg(pattern_frame, CODE_DIAMETER,
                            colors.pop(random.randint(0, len(colors) - 1)))
                            for i in range(num_holes)]
    for i in range(num_holes):
        hidden_row[i].configure(background=HIDDEN_COLOR)
        hidden_row[i].grid(row=0, column=i)
        if i < num_holes - 1:
            hidden_row[i].grid_configure(padx=(0, PEG_SPACING))

    # Create a row for the buttons
    button_frame = ttk.Frame(window)
    button_frame.grid(row=3, column=0, pady=(0, V_SPACING))
    button_row = [MButton(button_frame, BUTTON_DIAMETER, COLORS[i])
                    for i in range(num_colors)]
    for i in range(num_colors):
        button_row[i].grid(row=num_rows+1, column=i)
        button_row[i].bind('<ButtonPress>', place_peg)
        if i < num_colors - 1:
            button_row[i].grid_configure(padx=(0, PEG_SPACING))

    # Create Back and Confirm buttons
    options_frame = ttk.Frame(window)
    options_frame.grid(row=4, column=0)
    back_button = ttk.Button(options_frame, text='Back',
        command=back, state=DISABLED)
    back_button.grid(row=0, column=0, padx=(0, H_SPACING))
    confirm_button = ttk.Button(options_frame, text='Confirm',
        command=confirm, state=DISABLED)
    confirm_button.grid(row=0, column=1)

    # Center the window and prevent the window from shrinking too far
    root = window.master
    root.minsize(width=0, height=0)
    root.geometry('')
    root.update_idletasks()
    width = root.winfo_width()
    frm_width = root.winfo_rootx() - root.winfo_x()
    win_width = width + frm_width * 2
    height = root.winfo_height()
    tlb_height = root.winfo_rooty() - root.winfo_y()
    win_height = height + tlb_height + frm_width
    x = root.winfo_screenwidth() // 2 - win_width // 2
    y = root.winfo_screenheight() // 2 - win_height // 2
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.minsize(width=width, height=height)


def show_settings(root):
    """Opens a window with settings the user can configure."""
    global num_holes
    global num_colors
    global repeating_colors

    # Create the window
    window = Toplevel(root)
    window.title('Settings')

    # Create a label and combobox for setting repeating colors
    repeatingcolors_label = ttk.Label(window, text='Repeating colors')
    repeatingcolors_combobox = ttk.Combobox(window, values=('Yes', 'No'),
        state='readonly')
    repeatingcolors_combobox.set('Yes' if repeating_colors else 'No')

    # Create a label and combobox for setting holes
    holes_label = ttk.Label(window, text='Number of slots')
    holes_combobox = ttk.Combobox(window, values=list(range(3, 6+1)),
        state='readonly')
    holes_combobox.set(num_holes)

    # Create a label and combobox for setting colors
    colors_label = ttk.Label(window, text='Number of colors')
    colors_combobox = ttk.Combobox(window, values=list(range(2, 8+1)),
        state='readonly')
    colors_combobox.set(num_colors)

    # Create a warning label
    warning_label = ttk.Label(window, text='*New values for settings will ' + \
        'only take effect once you start a new game.')

    # Create a cancel button and a save changes button
    button_frame = ttk.Frame(window)
    cancel_button = ttk.Button(button_frame, text='Cancel', command=lambda:
        window.destroy())
    cancel_button.grid(row=0, column=0)
    def save_changes():
        # Set repeating colors
        global repeating_colors
        if colors_combobox.get() == 'Yes':
            repeating_colors = True
        else:
            repeating_colors = False
        # Set number of holes
        global num_holes; num_holes = int(holes_combobox.get())
        # Set number of colors
        global num_colors; num_colors = int(colors_combobox.get())
        # Prevent error
        if num_colors < num_holes and repeating_colors == False:
            repeating_colors = True
        window.destroy()
    save_button = ttk.Button(button_frame, text='Save', command=save_changes)
    save_button.grid(row=0, column=1)

    # Add the widgets to the grid
    repeatingcolors_label.grid(row=0, column=0, sticky=W)
    repeatingcolors_combobox.grid(row=1, column=0, sticky=W)
    holes_label.grid(row=2, column=0, sticky=W)
    holes_combobox.grid(row=3, column=0, sticky=W)
    colors_label.grid(row=4, column=0, sticky=W)
    colors_combobox.grid(row=5, column=0, sticky=W)
    warning_label.grid(row=6, column=0, sticky=W)
    button_frame.grid(row=7, column=0)

    # Center the window and prevent the it from shrinking too far
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
        '\\' + FILENAME, 'r')
    instructions_text = inputfile.read()
    inputfile.close()

    # Create text for the instructions
    instructions = Text(window, width=50, height=20, wrap=WORD,
        font=('Comic Sans MS', 12))
    instructions.insert(0.0, instructions_text)
    instructions['state'] = DISABLED
    instructions.grid(row=0, column=0, sticky=(N, S, E, W))

    # Create a scrollbar for the instructions
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL,
        command=instructions.yview)
    scrollbar.grid(column=1, row=0, sticky=(N, S))
    instructions['yscrollcommand'] = scrollbar.set

    # Create a button to exit
    ok_button = ttk.Button(window, text='OK', command=window.destroy)
    ok_button.grid(row=1, column=0, columnspan=2)

    # Center the window and prevent the window from shrinking too far
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


def place_peg(event):
    global code_grid
    global cur_row
    global cur_hole
    global back_button
    global confirm_button
    global game_over

    # Make sure the cursor is on a hole and the game is not over
    if cur_hole >= len(code_grid[0]) or game_over:
        return

    # Get the color of the pressed button
    color = event.widget.get_color()

    # Place a peg of the color on the current position on the board
    code_grid[cur_row][cur_hole].set_color(color)

    # Advance the cursor to the next peg
    cur_hole += 1

    # Enable the back button
    if cur_hole == 1:
        back_button['state'] = NORMAL
    
    # Enable the confirm button
    elif cur_hole == num_holes:
        confirm_button['state'] = NORMAL


def back():
    """Removes the last peg placed, if one exists in the row."""
    global code_grid
    global cur_row
    global cur_hole
    global back_button
    global confirm_button

    # Make sure the current hole is not at 0
    if cur_hole == 0:
        return
        
    # Decrement the cursor
    cur_hole -= 1

    # Revert the last peg placed to a hole
    code_grid[cur_row][cur_hole].set_color(HOLE_COLOR)

    # Disable the back button
    if cur_hole == 0:
        back_button['state'] = DISABLED
    
    # Disable the confirm button
    elif cur_hole == len(code_grid[0]) - 1:
        confirm_button['state'] = DISABLED


def confirm():
    """Sets the player's current guess and checks to see if won."""
    global key_grid
    global hidden_row
    global hidden_pattern
    global cur_row
    global cur_hole
    global game_over

    # Get the number of hits and blows
    hits, blows = check_winner()

    # Place key pegs indicating the number of hits and blows
    cur_key = 0
    for i in range(hits):
        key_grid[cur_row][cur_key].set_color(HIT_COLOR)
        cur_key +=1
    for i in range(blows):
        key_grid[cur_row][cur_key].set_color(BLOW_COLOR)
        cur_key +=1

    # Advance the cursor to the next row
    cur_row += 1
    cur_hole = 0

    # End the game if the player has won
    if hits == len(code_grid[0]):
        game_over = True
        message.set('Congratulations! You WON!')
    
    # End the game if the player has passed the last row
    elif cur_row == len(code_grid):
        game_over = True
        message.set('You lost. Better luck next time.')

    # Show the hidden pattern if game over
    if game_over:
        for i in range(len(code_grid[0])):
            hidden_row[i].set_color(hidden_pattern[i].get_color())

    # Disable the back and confirm buttons
    back_button['state'] = DISABLED
    confirm_button['state'] = DISABLED


def check_winner():
    """
    Checks to see if the player guessed the pattern correctly.
    Return: A tuple containing the number of hits and the number of blows
    """
    hits = 0
    blows = 0
    global code_grid; guess = list(code_grid[cur_row])      # Make list of player guess
    global hidden_pattern; pattern = list(hidden_pattern)   # Make list of hidden pattern

    # Calculate the number of hits
    i = 0
    while i < len(guess):
        if guess[i] == pattern[i]:
            hits += 1
            guess.pop(i)
            pattern.pop(i)
        else:
            i += 1
    
    # Calculate the number of blows
    i = 0
    while i < len(guess):
        for peg in pattern:
            if guess[i] == peg:
                blows += 1
                break
        i += 1

    # Return the number of hits and blows
    return hits, blows


def main():
    # Create the root
    root = Tk()
    root.title('Mastermind')

    # Create styles
    s = ttk.Style()
    s.configure('hidden.TFrame', background=HIDDEN_COLOR)

    # Make the window resizeable
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)

    # Create a menu bar
    root.option_add('*tearOff', FALSE)
    menubar = Menu(root)
    root['menu'] = menubar
    menu_game = Menu(menubar)
    menu_help = Menu(menubar)
    menubar.add_cascade(menu=menu_game, label='Game')
    menubar.add_cascade(menu=menu_help, label='Help')
    menu_game.add_command(label='New game', command=lambda:
        build_board(board))
    menu_game.add_command(label='Settings', command=lambda:
        show_settings(root))
    menu_game.add_command(label='Exit', command=lambda:
        root.destroy())
    menu_help.add_command(label='How to play', command=lambda:
        show_how_to_play(root))

    # Create a footer
    global footer_text; footer_text = StringVar(root)
    footer = ttk.Label(root, textvariable=footer_text)
    footer.grid(row=2, column=0, sticky=(S, W))

    # Create the board frame and display it
    board = ttk.Frame(root, padding=PADDING)
    board.grid(row=1, column=0)
    build_board(board)

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()