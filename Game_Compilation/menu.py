"""
File: menu.py
Author: Alex Gill
Displays a menu which allows the user to select one of several games
to play.
"""
from tkinter import *
from tkinter import ttk
from util.playsound import playsound
import threading
import pathlib
import os
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    from pygame import mixer
    from pygame.mixer import music
    music_imported = True
except ImportError:
    music_imported = False
    print('Pygame not imported')

# --- Global variables ---
games = None                # The list of games
game_frames = None          # Frames showing the labels
game_labels = None          # Labels showing a thumbnail and a name
game_thumbs = None          # The thumbnails for each label
leftbutton_label = None     # The left button label
rightbutton_label = None    # The right button label

# --- Global constants ---
MENU_PADDING = 20   # The padding around the whole window
ITEM_SPACING = 20   # The spacing between menu frames
GAME_PADDING = 5    # The padding around game frames
GRID_SPACING = 10   # The spacing between games in the grid

# --- App-related constants ---
APP1 = '..\\Snake\\snake.py'
APP1_NAME = 'Snake'
APP1_THUMB = 'THUMBNAILS\\app1.gif'
APP2 = '..\\Random_Sentence_Generator\\random_sentence_generator_gui.py'
APP2_NAME = 'Random Sentence Generator'
APP2_THUMB = 'THUMBNAILS\\app2.gif'
APP3 = '..\\Mastermind\\mastermind.py'
APP3_NAME = 'Mastermind'
APP3_THUMB = 'THUMBNAILS\\app3.gif'
APP4 = '..\\Hello_World\\hello.py'
APP4_NAME = 'Hello World'
APP4_THUMB = 'THUMBNAILS\\app4.gif'
APP5 = '..\\Hexapawn\\hexapawn.py'
APP5_NAME = 'Hexapawn'
APP5_THUMB = 'THUMBNAILS\\app5.gif'
APP6 = '..\\Choose_Your_Own_Adventure\\adventure.py'
APP6_NAME = 'Choose Your Own Adventure'
APP6_THUMB = 'THUMBNAILS\\app6.gif'
APP7 = '..\\Tic_tac_toe\\tic_tac_toe.py'
APP7_NAME = 'Tic-tac-toe'
APP7_THUMB = 'THUMBNAILS\\app7.gif'
APP8 = '..\\Blackjack\\blackjackgui.py'
APP8_NAME = 'Blackjack'
APP8_THUMB = 'THUMBNAILS\\app8.gif'
APP9 = '..\\Trivia_Game\\trivia.py'
APP9_NAME = 'Trivia Game'
APP9_THUMB = 'THUMBNAILS\\app9.gif'
BACKWARD_DISABLED = 'IMAGES\\backward_disabled.gif'
BACKWARD_ENABLED = 'IMAGES\\backward_enabled.gif'
FORWARD_DISABLED = 'IMAGES\\forward_disabled.gif'
FORWARD_ENABLED = 'IMAGES\\forward_enabled.gif'
MUSIC = 'AUDIO\\Gold_Saucer.mp3'
SOUND = 'AUDIO\\cursor.wav'

class rainbowtext(ttk.Frame):
    """A custom widget that displays text with letters alternating
    colors every period of time."""
    def __init__(self, master, text='Hello, world!',
                 colors=('red', 'green', 'blue', 'yellow'), size=32,
                 font='UD Digi Kyokasho NP-R', spacing=0, interval=1000):
        # Initialize the frame
        super().__init__(master)

        # Set the colors and the interval
        self.colors = colors
        self.starting_color = len(self.colors) - 1
        self.interval = interval

        # Create a label for each character in text
        self.letters = []
        color_index = 0
        for i in range(len(text)):
            self.letters.append(ttk.Label(self, text=text[i],
                font=(font, size), foreground=self.colors[color_index]))
            self.letters[i].grid(row=0, column=i,
                padx=(0, spacing) if i < len(text) - 1 else None)
            if color_index == len(self.colors) - 1: color_index = 0
            else: color_index += 1

        # Start the changing colors loop
        self.change_colors_task()

    def change_colors(self):
        """Rotates the current color combination."""
        color_index = self.starting_color
        for letter in self.letters:
            letter.configure(foreground=self.colors[color_index])
            if color_index == len(self.colors) - 1: color_index = 0
            else: color_index += 1
        if self.starting_color == 0: self.starting_color = len(self.colors) - 1
        else: self.starting_color -= 1

    def change_colors_task(self):
        """Rotates the current color combination repeatedly after the
        interval."""
        self.change_colors()
        self.master.after(self.interval, self.change_colors_task)


def open_app(event, root, app):
    """Opens the specified app."""
    # Hide the window
    root.withdraw()

    # Pause the music
    if music_imported:
        music.pause()

    # Open the game
    os.system('python "' + app + '"')

    # Show the window
    root.deiconify()

    # Play the music
    if music_imported:
        music.unpause()


def on_hover(event):
    """Executes when a game is hovered over by the mouse."""
    # Change the hand shape
    event.widget.configure(cursor='hand2')

    # Play the sound effect
    threading.Thread(target=play_sound).start()


def play_sound():
    """Plays the sound effect."""
    playsound(SOUND)


def button_press(event, page_num):
    """Moves to the specified page."""
    global game_frames
    global rightbutton_label
    global leftbutton_label
    for frame in game_frames:
        frame.grid_remove()

    # Make the button look pressed
    event.widget.master.configure(relief=SUNKEN)

    # Play the sound effect
    threading.Thread(target=play_sound).start()
        
    # Page 1
    if page_num == 1:
        # Put the first six games in the game frames
        for i in range(6):
            game_frames[i].grid()
    
    # Page 2
    elif page_num == 2:
        # Put the last three games in the game frames
        for i in range(3):
            game_frames[6 + i].grid()


def button_release(event, page_num):
    """To be executed when the button is released."""
    # Make the button look unpressed
    event.widget.master.configure(relief=RAISED)

    # Page 1
    if page_num == 1:
        # Change the button images
        global left_disabled
        global right_enabled
        leftbutton_label.configure(image=left_disabled)
        rightbutton_label.configure(image=right_enabled)
    
    # Page 2
    elif page_num == 2:
        # Change the button images
        global left_enabled
        global right_disabled
        leftbutton_label.configure(image=left_enabled)
        rightbutton_label.configure(image=right_disabled)


def play_music():
    """Starts the music."""
    if music_imported:
        mixer.init()
        music.load(MUSIC)
        music.play(loops=-1)


def stop(root):
    """Stops the music and closes the window."""
    if music_imported:
        music.stop()
        music.unload()
        mixer.quit()
    root.destroy()


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
    root.title('AJ\'s Fun House')
    root.protocol('WM_DELETE_WINDOW', lambda: stop(root))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)

    # The directory for the files
    dir = str(pathlib.Path(__file__).parent.resolve()) + '\\'

    # Instantiate the audio files
    global MUSIC; MUSIC = dir + MUSIC
    global SOUND; SOUND = dir + SOUND

    # Create the rainbow text
    title_frame = ttk.Frame(root)
    title_frame.grid(row=0, column=0, pady=(MENU_PADDING, ITEM_SPACING),
        sticky=N)
    title = rainbowtext(title_frame, text='A.J.\'s Fun House',
        colors=('red', 'blue', 'green', 'yellow', 'violet', 'orange'), size=44)
    title.grid()

    # Create the game thumbnails and labels
    games_frame = ttk.Frame(root)
    games_frame.grid(row=1, column=0,
        padx=MENU_PADDING, pady=(0, ITEM_SPACING))
    global games; games = []
    global game_frames; game_frames = [ttk.Frame(games_frame,
        padding=GAME_PADDING, relief=SOLID, borderwidth=5) for i in range(9)]
    global game_labels; game_labels = []
    global game_thumbs; game_thumbs = []
    games.append(APP1)
    game_thumbs.append(PhotoImage(file=dir+APP1_THUMB))
    game_labels.append(ttk.Label(game_frames[0], image=game_thumbs[0],
        text=APP1_NAME, compound=TOP))
    games.append(APP2)
    game_thumbs.append(PhotoImage(file=dir+APP2_THUMB))
    game_labels.append(ttk.Label(game_frames[1], image=game_thumbs[1],
        text=APP2_NAME, compound=TOP))
    games.append(APP3)
    game_thumbs.append(PhotoImage(file=dir+APP3_THUMB))
    game_labels.append(ttk.Label(game_frames[2], image=game_thumbs[2],
        text=APP3_NAME, compound=TOP))
    games.append(APP4)
    game_thumbs.append(PhotoImage(file=dir+APP4_THUMB))
    game_labels.append(ttk.Label(game_frames[3], image=game_thumbs[3],
        text=APP4_NAME, compound=TOP))
    games.append(APP5)
    game_thumbs.append(PhotoImage(file=dir+APP5_THUMB))
    game_labels.append(ttk.Label(game_frames[4], image=game_thumbs[4],
        text=APP5_NAME, compound=TOP))
    games.append(APP6)
    game_thumbs.append(PhotoImage(file=dir+APP6_THUMB))
    game_labels.append(ttk.Label(game_frames[5], image=game_thumbs[5],
        text=APP6_NAME, compound=TOP))
    games.append(APP7)
    game_thumbs.append(PhotoImage(file=dir+APP7_THUMB))
    game_labels.append(ttk.Label(game_frames[6], image=game_thumbs[6],
        text=APP7_NAME, compound=TOP))
    games.append(APP8)
    game_thumbs.append(PhotoImage(file=dir+APP8_THUMB))
    game_labels.append(ttk.Label(game_frames[7], image=game_thumbs[7],
        text=APP8_NAME, compound=TOP))
    games.append(APP9)
    game_thumbs.append(PhotoImage(file=dir+APP9_THUMB))
    game_labels.append(ttk.Label(game_frames[8], image=game_thumbs[8],
        text=APP9_NAME, compound=TOP))
    for frame in game_frames:
        frame.bind('<Enter>', on_hover)
        frame.bind('<ButtonPress>', lambda e:
            open_app(e, root,dir + games[game_frames.index(e.widget)]))
        frame.bind('<Leave>', lambda e:
            e.widget.configure(cursor=''))
    for label in game_labels:
        label.bind('<Enter>', lambda e:
            e.widget.master.configure(cursor='hand2'))
        label.bind('<ButtonPress>', lambda e:
            open_app(e, root, dir + games[game_frames.index(e.widget.master)]))
        label.grid()

    # Put the first six games in the game frame
    for i in range(6):
        row = i // 3
        col = i % 3
        game_frames[i].grid(row=row, column=col, padx=(0, GRID_SPACING)
            if col < 2 else None, pady=(0, GRID_SPACING) if row < 1 else None)
    for i in range(3):
        row = i // 3
        col = i % 3
        game_frames[6 + i].grid(row=row, column=col, padx=(0, GRID_SPACING)
            if col < 2 else None)
    for i in range(3):
        game_frames[6 + i].grid_remove()

    # Create the back and forward buttons
    buttons_frame = ttk.Frame(root)
    buttons_frame.grid(row=2, column=0, pady=(0, MENU_PADDING), sticky=S)
    leftbutton_frame = ttk.Frame(buttons_frame, relief=RAISED, borderwidth=1)
    leftbutton_frame.grid(row=0, column=0)
    rightbutton_frame = ttk.Frame(buttons_frame, relief=RAISED, borderwidth=1)
    rightbutton_frame.grid(row=0, column=1)
    global left_disabled; left_disabled = PhotoImage(
        file=dir+BACKWARD_DISABLED)
    global left_enabled; left_enabled = PhotoImage(
        file=dir+BACKWARD_ENABLED)
    global right_disabled; right_disabled = PhotoImage(
        file=dir+FORWARD_DISABLED)
    global right_enabled; right_enabled = PhotoImage(
        file=dir+FORWARD_ENABLED)
    global leftbutton_label; leftbutton_label = ttk.Label(
        leftbutton_frame, image=left_disabled)
    leftbutton_label.grid()
    global rightbutton_label; rightbutton_label = ttk.Label(
        rightbutton_frame, image=right_enabled)
    rightbutton_label.grid()
    leftbutton_label.bind('<ButtonPress>', lambda e: button_press(e, 1))
    leftbutton_label.bind('<ButtonRelease>', lambda e: button_release(e, 1))
    rightbutton_label.bind('<ButtonPress>', lambda e: button_press(e, 2))
    rightbutton_label.bind('<ButtonRelease>', lambda e: button_release(e, 2))

    # Set the window resize properties.
    set_window_resize(root)

    # Play the music
    play_music()

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()
