"""
Program: adventure.py
Author: Alex Gill
Choose your own adventure.
"""
from tkinter import *
from tkinter import ttk
from scene import Scene
import pathlib

# --- Global constants ---
WIDTH = 400             # The width of the window
HEIGHT = 400            # The height of the window
FILENAME = 'scenes.txt' # The file name

# --- Global variables ---
scenes = None           # A list of all scenes
cur_scene = None        # To hold the current scene
body_text = None        # The text of the body being displayed
option1_text = None     # The text of the option 1 button
option2_text = None     # The text of the option 2 button
option1 = None          # The option 1 button
option2 = None          # The option 2 button

def build_gui(root):
    """Builds the GUI on the specified window."""
    global scenes
    global cur_scene

    # Create the label for the story text
    global body_text; body_text = StringVar()
    body = ttk.Label(root, textvariable=body_text, style='body.TLabel')
    body.grid(row=0, column=0)
    root.grid_rowconfigure(0, weight=9)

    # Create the option buttons
    global option1_text; option1_text = StringVar()
    global option1; option1 = ttk.Button(root, textvariable=option1_text,
        style='option.TButton',
        command=lambda: next_scene(scenes.index(cur_scene) * 2 + 1))
    option1.grid(row=1, column=0)
    root.grid_rowconfigure(1, weight=1)
    global option2_text; option2_text = StringVar()
    global option2; option2 = ttk.Button(root, textvariable=option2_text,
        style='option.TButton',
        command=lambda: next_scene(scenes.index(cur_scene) * 2 + 2))
    option2.grid(row=2, column=0)
    root.grid_rowconfigure(2, weight=1)


def play_again():
    """Starts the adventure again."""
    # Reset the current scene to the starting scene
    global scenes
    global cur_scene; cur_scene = scenes[0]
    
    # Set the text for the story text
    global body_text; body_text.set(scenes[0].body)
    global option1_text; option1_text.set(scenes[1].title)
    global option2_text; option2_text.set(scenes[2].title)

    # Reset the commands of the buttons
    global option1; option1.configure(
        command=lambda: next_scene(scenes.index(cur_scene) * 2 + 1))
    global option2; option2.configure(
        command=lambda: next_scene(scenes.index(cur_scene) * 2 + 2))
    option2.grid()


def next_scene(index):
    """Sets the GUI to display the scene. at the specified index."""
    # Set the current scene
    global scenes
    global cur_scene
    cur_scene = scenes[index]

    # Change the body text
    global body_text; body_text.set(cur_scene.get_body())

    # Change the option texts
    global option1_text
    global option1
    global option2_text
    if index * 2 + 1 < len(scenes):
        option1_text.set(scenes[index * 2 + 1].get_title())
        option2_text.set(scenes[index * 2 + 2].get_title())
    else:
        body_text.set(cur_scene.get_body() + '\n\nThe End')
        option1_text.set('Play Again')
        option1.configure(command=play_again)
        option2.grid_remove()


def read_scenes(filename):
    """Reads the scenes from a text file to a list."""
    # Create a list of scenes
    scenes = []

    # Open the file
    path = str(pathlib.Path(__file__).parent.resolve()) + '\\' + filename
    file = open(path, 'r')

    # Read the scenes from the file into the dictionary
    id = file.readline()    # Perform a priming read
    while id != '':
        id = int(id.strip())
        title = file.readline().strip()
        body = file.readline().strip()
        body = body.replace('\\t', '\t')
        body = body.replace('\\n', '\n')
        scenes.append(Scene(title, body))
        if len(scenes) - 1 != id:
            print('Something is wrong with the text file...')
            exit()
        file.readline() # Skip a line
        id = file.readline()

    # Return the dictionary
    return scenes


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
    root.title('Choose your own Adventure')
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    root.grid_columnconfigure(0, weight=1)

    # Create styles
    s = ttk.Style(root)
    s.configure('body.TLabel', font=('', 12), wraplength=WIDTH-2)
    s.configure('option.TButton', font=('', 12), wraplength=HEIGHT-2)

    # Read the scenes from the file
    global scenes; scenes = read_scenes(FILENAME)

    # Build the GUI
    build_gui(root)

    # Set the current scene
    global cur_scene; cur_scene = scenes[0]
    body_text.set(scenes[0].get_body())
    option1_text.set(scenes[1].get_title())
    option2_text.set(scenes[2].get_title())
    
    # Set the root window's resize properties
    set_window_resize(root)

    # Start the event loop
    root.mainloop()

if __name__ == '__main__':
    main()