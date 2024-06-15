"""
File: peg.py
Author: Alex Gill
Used to build a peg of a particular color in the Mastermind
game.
"""
from tkinter import *

class MPeg(Canvas):
    def __init__(self, master, diameter, color):
        # Set the color
        self.color = color

        # Set the diameter
        self.diameter = diameter
        
        # Initialize the canvas
        super().__init__(master, width=diameter, height=diameter, highlightthickness=0, borderwidth=0)

        # Draw the peg
        self.create_oval(1, 1, diameter-1, diameter-1, fill=color, outline='')

    def get_color(self):
        """Returns the color of the peg."""
        return self.color

    def set_color(self, color):
        """Sets the color of the peg."""
        self.color = color
        self.delete('all')
        self.create_oval(1, 1, self.diameter-1, self.diameter-1, fill=color, outline='')

    def __eq__(self, other):
        """Compares two peg objects."""
        return self.color == other.color

if __name__ == '__main__':
    """Test the class."""
    # Create the root
    root = Tk()
    root.title('Peg Test')

    # Create a peg and display it
    b = MPeg(root, 250, 'red')
    b.grid(padx=25, pady=25)

    # Start the event loop
    root.mainloop()