"""
File: matchbox.py
Author: Alex Gill
Represents a matchbox with a board configuration and beads that can be
removed and inserted to alter the probability of the opponent making
certain moves.
"""
from board import Board
import random

NUM_BEADS = 1   # The number of beads each move starts out with

class Matchbox:
    def __init__(self, move, board, possible_moves):
        """Creates a matchbox of the given board configuration with
        a dictionary of possible moves as its key and beads as its
        value."""
        self.move = move
        self.board_configuration = board
        self.possible_moves = {}
        for move in possible_moves:
            self.possible_moves[move] = 1

    def get_bead(self):
        """Gets a random move's bead to decide a move in the game."""
        potential_moves = []
        for key in self.possible_moves:
            for num_beads in range(self.possible_moves[key]):
                potential_moves.append(key)
        return random.choice(potential_moves)

    def add_bead(self, move):
        """Adds a bead to the given move."""
        self.possible_moves[move] += 1

    def remove_bead(self, move):
        """Removes a bead from the given move."""
        if self.possible_moves[move] > 0:
            self.possible_moves[move] -= 1


if __name__ == '__main__':
    """Test the class."""
    from tkinter import *
    from tkinter import ttk
    from board import Board
    import pathlib

    index = 23

    root = Tk()
    root.title('matchbox test')

    path = str(pathlib.Path(__file__).parent.resolve()) + '\\matchboxes.txt'
    frames = [ttk.Frame(root) for i in range(24)]
    matchboxes = {2:[], 4:[], 6:[]}
    file = open(path)

    file.readline()
    line_number = 1
    move_num = file.readline().strip()
    line_number += 1
    i = 0
    while move_num != '':
        move_num = int(move_num)
        if move_num != 2 and move_num != 4 and move_num != 6:
            print('wrong move on line', line_number)
            exit()
        pawns = file.readline().strip().split()
        line_number += 1
        if len(pawns) != 9:
            print('wrong number of pawns on line', line_number)
            exit()
        moves = file.readline().strip().split(',')
        line_number += 1
        possible_moves = []
        for move in moves:
            cur_move = move.split()
            for j in range(len(cur_move)):
                cur_move[j] = int(cur_move[j])
            possible_moves.append(tuple(cur_move))
        for move in possible_moves:
            if len(move) != 4:
                print('wrong number of rowcol indexes on line', line_number)
                exit()
        matchboxes[move_num].append(Matchbox(move_num, Board(frames[i], pawns),
                                    possible_moves))
        file.readline()
        line_number += 1
        move_num = file.readline().strip()
        line_number += 1
        i += 1
    
    if index < 2:
        move_num = 2
        matchbox_index = index
    elif index < 13:
        move_num = 4
        matchbox_index = index - 2
    else:
        move_num = 6
        matchbox_index = index - 13
    matchboxes[move_num][matchbox_index].board_configuration.grid(
                                        row=0, column=0)
    for i in range(len(matchboxes[move_num][matchbox_index].possible_moves)):
        new_board = Board(pawns=matchboxes[move_num][matchbox_index].
                                        board_configuration.starting_pawns)
        pm = list(matchboxes[move_num][matchbox_index].possible_moves.keys())
        new_board.pawn_move(pm[i][0], pm[i][1], pm[i][2], pm[i][3])
        new_board.grid(row=1, column=i)
    frames[index].grid(row=0, column=0)
    root.mainloop()