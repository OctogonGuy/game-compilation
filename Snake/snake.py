"""
File: snake.py
Author: Alex Gill
Simulates a game of snake.
"""
from tkinter import *
from tkinter import ttk
import random

# --- Global constants ---
ROWS = 19       # The width of the map in tiles
COLS = 29       # The height of the map in tiles
SIZE = 16       # The width and height of the tiles in pt
E = 0           # East
N = 1           # North
W = 2           # West
S = 3           # South
GROUND = '地'   # The character for ground
WALL = '壁'     # The character for wall
HEAD = '頭'     # The character for head
BODY = '身'     # The character for body
FOOD = '食'     # The character for food
EASY_FOOD = 7   # The number of food on the screen on easy
MEDM_FOOD = 3   # The number of food on the screen on medium
HARD_FOOD = 1   # The number of food on the screen on hard
EASY_TIME = 200 # The interval after which the snake will move on easy
MEDM_TIME = 100 # The interval after which the snake will move on medium
HARD_TIME = 50  # The interval after which the snake will move on hard

# --- Global variables ---
tiles = None        # The tiles on the map
head = None         # The x and y coordinates of the snake's head
body = None         # The x and y coordinates of each tile in the snake's body
tail = None         # The x and y coordinates of the snake's tail
prev_dir = N        # The previous direction the snake was heading
curr_dir = N        # The current direction the snake is heading
game_over = False   # Indicates whether the player has lose
difficulty = None   # The mode (E, M, or H)
food = MEDM_FOOD    # The number of food on the screen
time = MEDM_TIME    # The interval after which the snake will move

# --- GUI components ---
game_over_window = None # The window that appears when the player loses

def build_map(window):
    """Instantiate the tiles and place them on the grid."""
    global tiles; tiles = [[ttk.Label(window, text=GROUND,
        style='ground.TLabel') for j in range(COLS)] for i in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            tiles[i][j].grid(row=i, column=j)

def start_game():
    """Builds the map."""
    global tiles
    global body
    global head
    global tail

    # Create the ground
    for i in range(ROWS):
        for j in range(COLS):
            tiles[i][j].configure(text=GROUND, style='ground.TLabel')

    # Create the wall
    for i in range(COLS):
        tiles[0][i].configure(text=WALL, style='wall.TLabel')
    for i in range(1, ROWS):
        tiles[i][-1].configure(text=WALL, style='wall.TLabel')
    for i in range(COLS - 1):
        tiles[-1][i].configure(text=WALL, style='wall.TLabel')
    for i in range(1, ROWS - 1):
        tiles[i][0].configure(text=WALL, style='wall.TLabel')

    # Place the head of the snake
    head = {'x': COLS//2, 'y': ROWS - 4}
    tiles[head['y']][head['x']].configure(text=HEAD, style='head.TLabel')

    # Instantiate the body as an empty list
    body = []

    # Place the tail of the snake
    tail = {'x': head['x'], 'y': head['y'] + 1}
    tiles[tail['y']][tail['x']].configure(text=BODY, style='body.TLabel')

    # Place food
    for i in range(food):
        place_food()

    # Reset the direction
    global prev_dir; prev_dir = N
    global curr_dir; curr_dir = N


def show_game_over_window(root):
    """Builds the window that will appear when the player loses."""
    global difficulty
    global body

    # Create the window
    global game_over_window; game_over_window = Toplevel(root)
    game_over_window.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
    game_over_window.title('Game over')

    # Place the window inside the root window
    root_geom = root.geometry()
    root_geom = root_geom.replace('+', 'x')
    components = root_geom.split('x')
    for i in range(len(components)):
        components[i] = int(components[i])
    width = components[0] // 2
    height = components[1] // 2
    x = components[2] + width // 2
    y = components[3] + height // 2
    game_over_window.geometry(str(width) + 'x' + str(height) + \
        '+' + str(x) + '+' + str(y))

    # Make the window resizeable
    game_over_window.columnconfigure(0, weight=1)
    game_over_window.rowconfigure(0, weight=8)
    game_over_window.rowconfigure(1, weight=1)
    game_over_window.rowconfigure(2, weight=1)

    # Create a frame for the title and subtitle
    message_frame = ttk.Frame(game_over_window)
    message_frame.grid(row=0, column=0)

    # Create the title
    title = ttk.Label(message_frame, text='Game over', style='title.TLabel')
    title.grid(row=0, column=0)

    # Create the subtitle
    subtitle = ttk.Label(message_frame, text='Your score: ' + str(len(body)),
        style='subtitle.TLabel')
    subtitle.grid(row=1, column=0)

    # Create the difficulty radio buttons
    difficulty_frame = ttk.Frame(game_over_window)
    difficulty_frame.grid(row=1, column=0)
    easy = ttk.Radiobutton(difficulty_frame, text='Easy',
        variable=difficulty, value='E')
    easy.grid(row=0, column=0)
    medium = ttk.Radiobutton(difficulty_frame, text='Medium',
        variable=difficulty, value='M')
    medium.grid(row=0, column=1)
    hard = ttk.Radiobutton(difficulty_frame, text='Hard',
        variable=difficulty, value='H')
    hard.grid(row=0, column=2)

    # Create the play again button
    play_again_button = ttk.Button(game_over_window, text='Play again',
        command=play_again)
    play_again_button.grid(row=2, column=0)


def countdown(root, interval, num):
    """Starts a countdown."""
    countdown_label = ttk.Label(root, style='countdown.TLabel')
    countdown_label.grid(row=0, column=0)
    countdown_helper(root, countdown_label, interval, num)


def countdown_helper(root, label, interval, num):
    """Calls itself, decrementing num until num is 0, in which case it
    says 'GO' and starts the snake's movement."""
    if num > 0:
        label.configure(text=num)
        root.after(interval, lambda: countdown_helper(root, label, interval,
            num - 1))
    elif num == 0:
        label.configure(text='GO!')
        root.after(interval, lambda: countdown_helper(root, label, interval,
            num - 1))
    else:
        label.grid_forget()
        keep_moving(tiles[0][0].master.master)


def play_again():
    """Starts the game over again."""
    global food
    global time
    global game_over; game_over = False

    # Set the difficulty
    if difficulty.get() == 'E':
        food = EASY_FOOD
        time = EASY_TIME
    elif difficulty.get() == 'M':
        food = MEDM_FOOD
        time = MEDM_TIME
    elif difficulty.get() == 'H':
        food = HARD_FOOD
        time = HARD_TIME

    # Reset the window
    game_over_window.destroy()
    start_game()

    # Start the countdown which then starts the snake's movement.
    countdown(tiles[0][0].master.master, time * 5, 3)


def move():
    """Moves the snake in the given direction."""
    global tiles
    global head
    global body
    global tail
    global prev_dir
    global curr_dir
    global game_over

    ate = False    # Indicates whether the snake ate a pellet

    # Prevent the snake from moving backwords, running into a wall, or
    # running into itself. Also, figure out if the snake has eaten.
    if curr_dir == N:
        if prev_dir == S:
            return
        if head['y'] - 1 == 0 or \
           tiles[head['y'] - 1][head['x']]['text'] == BODY and (
                (tail['x'], tail['y']) != (head['x'], head['y'] - 1)):
            game_over = True
            return
        if tiles[head['y'] - 1][head['x']]['text'] == FOOD:
            ate = True
    elif curr_dir == S:
        if prev_dir == N:
            return
        if head['y'] + 1 == ROWS - 1 or \
           tiles[head['y'] + 1][head['x']]['text'] == BODY and (
                (tail['x'], tail['y']) != (head['x'], head['y'] + 1)):
            game_over = True
            return
        if tiles[head['y'] + 1][head['x']]['text'] == FOOD:
            ate = True
    elif curr_dir == E:
        if prev_dir == W:
            return
        if head['x'] + 1 == COLS - 1 or \
           tiles[head['y']][head['x'] + 1]['text'] == BODY and (
                (tail['x'], tail['y']) != (head['x'] + 1, head['y'])):
            game_over = True
            return
        if tiles[head['y']][head['x'] + 1]['text'] == FOOD:
            ate = True
    elif curr_dir == W:
        if prev_dir == E:
            return
        if head['x'] - 1 == 0 or \
           tiles[head['y']][head['x'] - 1]['text'] == BODY and (
                (tail['x'], tail['y']) != (head['x'] - 1, head['y'])):
            game_over = True
            return
        if tiles[head['y']][head['x'] - 1]['text'] == FOOD:
            ate = True

    # Move the tail in the direction of last body tile if it did not eat
    if not ate:
        tiles[tail['y']][tail['x']].configure(text=GROUND,
            style='ground.TLabel')
        if len(body) > 0:
            tail['x'] = body[-1]['x']
            tail['y'] = body[-1]['y']
        else:
            tail['x'] = head['x']
            tail['y'] = head['y']

    # Add body if the snake ate
    else:
        body.append({'x': tail['x'], 'y': tail['y']})

    # Move each body tile in the direction of its predecessor
    for i in range(len(body) - 1, -1, -1):
        if i > 0:
            body[i]['x'] = body[i - 1]['x']
            body[i]['y'] = body[i - 1]['y']
        else:
            body[i]['x'] = head['x']
            body[i]['y'] = head['y']

    # Move the head in the specified direction
    tiles[head['y']][head['x']].configure(text=BODY, style='body.TLabel')
    if curr_dir == N:
        head['y'] -= 1
    elif curr_dir == S:
        head['y'] += 1
    elif curr_dir == E:
        head['x'] += 1
    elif curr_dir == W:
        head['x'] -= 1
    tiles[head['y']][head['x']].configure(text=HEAD, style='head.TLabel')

    # Place food
    if ate:
        place_food()

    # Set the current direction
    prev_dir = curr_dir


def keep_moving(root):
    """Calls the move function repeatedly after an interval of time."""
    global game_over

    # Move the snake
    move()

    # Move the snake after the interval
    if not game_over:
        root.after(time, lambda: keep_moving(root))

    # If game over, display a message
    else:
        show_game_over_window(root)


def change_direction(dir):
    """Changes the direction the snake is heading."""
    global prev_dir
    global curr_dir

    # Change the snake's direction unless the direction is backwards
    if dir == N and prev_dir != S:
        curr_dir = N
    elif dir == S and prev_dir != N:
        curr_dir = S
    elif dir == E and prev_dir != W:
        curr_dir = E
    elif dir == W and prev_dir != E:
        curr_dir = W


def place_food():
    """Places food in a random tile on the map."""
    global tiles

    # Create a list of coordinates of unoccupied tiles
    available_coords = []
    for i in range(ROWS):
        for j in range(COLS):
            if tiles[i][j]['text'] == GROUND:
                available_coords.append({'x': j, 'y': i})
    
    # Place the food at a random unoccupied tile
    coords = random.choice(available_coords)
    tiles[coords['y']][coords['x']].configure(text=FOOD, style='food.TLabel')


def center_window(window):
    """Centers the window."""
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


def main():
    # Create the root
    root = Tk()
    root.title('Snake')
    root.resizable(False, False)

    # Create the styles
    s = ttk.Style()
    s.configure('TLabel', font=('MS PGothic', SIZE), background='#050b0f')
    s.configure('ground.TLabel', foreground='#0a151e')
    s.configure('wall.TLabel', foreground='#306998')
    s.configure('head.TLabel', foreground='#ffd43b')
    s.configure('body.TLabel', foreground='#ffe873')
    s.configure('food.TLabel', foreground='#e6e6e6')
    s.configure('title.TLabel', font=('Calibri', 32), background=
        s.lookup('TFrame', 'background'))
    s.configure('subtitle.TLabel', font=('Calibri', 18), background=
        s.lookup('TFrame', 'background'))
    s.configure('countdown.TLabel', font=('Calibri', 64), foreground='red')

    # Create the main frame
    mainframe = ttk.Frame(root)
    mainframe.grid(row=0, column=0)

    # Build the map
    build_map(mainframe)

    # Add key bindings
    root.bind('<KeyPress-Up>', func=lambda e: change_direction(N))
    root.bind('<KeyPress-Down>', func=lambda e: change_direction(S))
    root.bind('<KeyPress-Right>', func=lambda e: change_direction(E))
    root.bind('<KeyPress-Left>', func=lambda e: change_direction(W))

    # Initialize the difficulty
    global difficulty; difficulty = StringVar(value='M')

    # Create the game
    start_game()

    # Start the countdown which then starts the snake's movement.
    countdown(root, time * 5, 3)

    # Center the window
    center_window(root)

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()