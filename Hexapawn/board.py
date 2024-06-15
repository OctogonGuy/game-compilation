"""
File: board.py
Author: Alex Gill
A board in the game of hexapawn with nxm squares.
"""
from tkinter import *
from tkinter import ttk
from square import Square

class Board(ttk.Frame):
    def __init__(self, master=None, pawns=['b', 'b', 'b',
                                           'e', 'e', 'e',
                                           'w', 'w', 'w']):
        """Creates a board the given pawn configuration."""
        # Initialize the frame
        super().__init__(master)

        # Set the rows and cols
        self.rows = 3
        self.cols = 3

        # Initialize the squares, alternating white and black background
        self.squares = [[Square(self, i, j) for j in range(self.rows)] \
            for i in range(self.cols)]
        cur_bg = 'white'
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].set_background(cur_bg)
                if cur_bg == 'white':
                    cur_bg = 'black'
                else:
                    cur_bg = 'white'

        # Place the pawns
        for i in range(len(pawns)):
            if pawns[i] == 'b':
                pawns[i] = 'black'
            elif pawns[i] == 'w':
                pawns[i] = 'white'
            elif pawns[i] == 'e':
                pawns[i] = 'empty'
        self.starting_pawns = pawns

        # Place the squares on the grid
        pawn_index = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].set_pawn(pawns[pawn_index])
                self.squares[i][j].grid(row=i, column=j)
                pawn_index += 1

    def pawn_move(self, from_row, from_col, to_row, to_col):
        """Moves a pawn at a position to a new position."""
        # Get the pawn color
        color = self.squares[from_row][from_col].pawn

        # Remove the pawn from the current space
        self.squares[from_row][from_col].set_pawn('empty')

        # Place the pawn at the new space
        self.squares[to_row][to_col].set_pawn(color)

    def square_empty(self, row, col):
        """Returns True if the square at the specified position is
        empty."""
        square_photo = self.squares[row][col].photo
        if square_photo == None:
            return True
        else:
            return False
    
    def reset(self):
        """Resets the board configuration to starting positions."""
        # The pawn configuration
        pawns = ['black', 'black', 'black',
                 'empty', 'empty', 'empty',
                 'white', 'white', 'white']

        # Place the squares on the grid
        pawn_index = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].set_pawn(pawns[pawn_index])
                self.squares[i][j].grid(row=i, column=j)
                pawn_index += 1

    def reverse(self):
        """Returns the board flipped horizontally."""
        c = self.squares    # Board configuration
        r_board = Board(pawns=(c[0][2].pawn, c[0][1].pawn, c[0][0].pawn,
                               c[1][2].pawn, c[1][1].pawn, c[1][0].pawn,
                               c[2][2].pawn, c[2][1].pawn, c[2][0].pawn))
        return r_board

    def __eq__(self, other):
        """Compares boards for equal configurations."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].pawn != other.squares[i][j].pawn:
                    return False
        return True


if __name__ == '__main__':
    """Test the class."""
    # Create the root
    root = Tk()
    root.title('Board test')

    # Create a board and display it
    board = Board(root)
    board.grid(row=0, column=0)

    # Move the player's middle pawn forward
    board.pawn_move(2, 1, 1, 1)

    # Print square_empty for each square
    for i in range(3):
        for j in range(3):
            print(i, j, 'Empty' if board.square_empty(i, j) else 'Occupied')

    # Create a new board and test for equality
    board2 = Board(root)
    print(board == board2)
    board2.pawn_move(2, 1, 1, 1)
    print(board == board2)

    # Start the event loop
    root.mainloop()