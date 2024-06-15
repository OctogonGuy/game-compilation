"""
File: square.py
Author: Alex Gill
A tile with a black pawn, white pawn, or no pawn in the game of
hexapawn.
"""
from tkinter import *
import pathlib

class Square(Canvas):
    def __init__(self, master, row, col, background='white', pawn=None):
        # Initialize the canvas
        super().__init__(master, width=100, height=100, \
            highlightthickness=0, borderwidth=0)

        # Set the row and column
        self.row = row
        self.col = col

        # Set the background
        self['background'] = background

        # Display the image
        if pawn == 'black':
            path = str(pathlib.Path(__file__).parent.resolve()) + \
                '\\PIECES\\black_pawn.gif'
            self.pawn = pawn
            self.photo = PhotoImage(file=path)
        elif pawn == 'white':
            path = str(pathlib.Path(__file__).parent.resolve()) + \
                '\\PIECES\\white_pawn.gif'
            self.pawn = pawn
            self.photo = PhotoImage(file=path)
        else:
            self.pawn = None
            self.photo = None
        self.create_image(50, 50, image=self.photo)

    def set_background(self, background):
        self['background'] = background

    def set_pawn(self, pawn):
        """Sets the graphic to a black pawn, white pawn, or empty."""
        # Display the image
        if pawn == 'black':
            path = str(pathlib.Path(__file__).parent.resolve()) + \
                '\\PIECES\\black_pawn.gif'
            self.pawn = pawn
            self.photo = PhotoImage(file=path)
        elif pawn == 'white':
            path = str(pathlib.Path(__file__).parent.resolve()) + \
                '\\PIECES\\white_pawn.gif'
            self.pawn = pawn
            self.photo = PhotoImage(file=path)
        else:
            self.pawn = None
            self.photo = None
        self.delete('all')
        self.create_image(50, 50, image=self.photo)

    
if __name__ == '__main__':
    """Test the class."""
    # Create the root
    root = Tk()
    root.title('Pawn test')

    # Create a black pawn and display it
    blackpawn = Square(root, 0, 0, 'yellow', 'black')
    blackpawn.grid(row=0, column=0)

    # Create a white pawn and display it
    whitepawn = Square(root, 0, 1, 'green', 'white')
    whitepawn.grid(row=0, column=1)

    # Print the pawn colors
    print(blackpawn.pawn)
    print(whitepawn.pawn)

    # Start the event loop
    root.mainloop()