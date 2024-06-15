"""
Program: hello.py
Author: Alex Gill
Displays a message in a window.
"""
from tkinter import *
from tkinter import ttk
from tkinter import font
import os
import random

MESSAGE = "Hello, world!"   # The message
MESSAGE_USR = 'Hello, ' + os.environ['USERNAME'] + '!'
FONT_SIZE = 64              # The font size
FONT = 'Eras Bold ITC'      # The default font family
COLOR = 'indigo'            # The default font color
SPACING = 5                 # The spacing between each letter (in pixels)
PADDING = 100               # The padding (in pixels)

chars = []                                      # Contains labels for each char
colors = [COLOR for i in range(len(MESSAGE))]   # Current color for each char
fonts = []                                      # The list of available fonts

def lighten_color(widget):
    """Makes the color of the widget lighter."""
    amount = 0.30   # The percent by which to lighten the color

    # Get the RGB values from the calling widget
    (r, g, b) = widget.winfo_rgb(widget['foreground'])

    # Convert the RGB values to range 255
    r //= 256
    g //= 256
    b //= 256

    # Increase the RGB values based on the amount
    r += round((255 - r) * amount)
    g += round((255 - g) * amount)
    b += round((255 - b) * amount)

    # Apply the new color to the widget
    widget['foreground'] = ('#%02x%02x%02x' % (r, g, b))


def revert_color(widget):
    """Reverts a widget's color from its lightened state."""
    index = chars.index(widget)
    widget.configure(foreground=colors[index])


def change_color(widget):
    """Changes the color of the widget to a random color."""

    # Randomly select the RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Set the new color value
    index = chars.index(widget)
    colors[index] = '#%02x%02x%02x' % (r, g, b)

    # Apply the new color to the widget
    widget['foreground'] = (colors[index])


def set_window_resize(window):
    """Centers the window and prevents it from shrinking past the
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


def change_font():
    """Changes the font of the style to a random font."""
    # Change the font
    style.configure('TLabel', font=(random.choice(fonts), FONT_SIZE))
    print(style.lookup('TLabel', 'font'))

    # Resize the window
    root.minsize(width=0, height=0)
    root.geometry('')

    # Reset the resize properties of the root window
    set_window_resize(root)


def on_enter(event):
    """Performed when the pointer enters the widget."""
    event.widget.configure(cursor='hand2')
    lighten_color(event.widget)


def on_leave(event):
    """Performed when the pointer leaves the widget."""
    event.widget.configure(cursor='')
    revert_color(event.widget)


def on_click(event):
    """Performed when a mouse button is pressed on the widget."""
    change_color(event.widget)
    lighten_color(event.widget)


def on_keypress(event):
    """Performed when a keyboard key is pressed."""
    change_font()


def main():
    # Create the root
    global root; root = Tk()
    root.title('Hello World')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.bind('<KeyPress>', on_keypress)

    # Fill the fonts list
    for family in font.families():
        fonts.append(family)

    # Create the frame
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=PADDING, pady=PADDING)

    # Create the label style
    global style; style = ttk.Style()
    style.configure('TLabel', font=(FONT, FONT_SIZE))

    # Create the label and display it on the grid
    for i in range(len(MESSAGE_USR)):
        chars.append(ttk.Label(frame, text=MESSAGE_USR[i], foreground=COLOR))
        chars[i].grid(column=i, row=0, padx = (SPACING, 0) if i != 0 else None)

    # Bind events to each label
    for i in range(len(chars)):
        chars[i].bind('<Enter>', on_enter)
        chars[i].bind('<Leave>', on_leave)
        chars[i].bind('<ButtonPress>', on_click)

    # Set the resize properties of the root window
    set_window_resize(root)

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()