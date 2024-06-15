"""
File: button.py
Author: Alex Gill
Used to build a pressable Button of a particular color in
the Mastermind game.
"""
from tkinter import *

class MButton(Canvas):
    def __init__(self, master, diameter, color):
        # Set the color
        self.color = color

        # Initialize the canvas
        super().__init__(master, width=diameter, height=diameter, highlightthickness=0, borderwidth=0)

        # Add the outer frame around the button
        self.create_oval(1, 1, diameter-1, diameter-1, fill='gray', outline='', tags=('buttonpart'))

        # Add the inner frame around the button
        self.create_oval(diameter * 0.1+1, diameter * 0.1+1, diameter * 0.9-1, diameter * 0.9-1, fill='darkgray', outline='', tags=('buttonpart'))

        # Add the button itself
        self.create_oval(diameter * 0.2+1, diameter * 0.2+1, diameter * 0.8-1, diameter * 0.8-1, fill=color, outline='', tags=('buttonpart'))

        # Make the cursor change when hovering over the button
        self.bind('<Enter>', lambda event: event.widget.configure(cursor='hand2'))
        self.bind('<Leave>', lambda event: event.widget.configure(cursor=''))

    def bind(self, sequence, func):
        """Binds an event to just the button parts."""
        self.tag_bind('buttonpart', sequence, func)

    def get_color(self):
        """Returns the color of the button."""
        return self.color

if __name__ == '__main__':
    """Test the class."""
    # Create the root
    root = Tk()
    root.title('Button Test')

    # Create a button and display it
    b = MButton(root, 250, 'red')
    b.grid(padx=25, pady=25)

    # Start the event loop
    root.mainloop()