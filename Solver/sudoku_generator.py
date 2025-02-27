# !/usr/bin/python
from Sudoku.Generator import *


class SudokuGenerator():

    # setting difficulties and their cutoffs for each solve method
    difficulties = {
        'easy': (35, 0),
        'medium': (81, 5),
        'hard': (81, 10),
        'extreme': (81, 15)
    }

    def __init__(self, difficulty):
        # Set the desired diffuculty
        self.difficulty = self.difficulties[difficulty]

    def set_difficulty(self, difficulty):
        # Set the desired diffuculty
        self.difficulty = self.difficulties[difficulty]

    def get_sudoku(self):
        # constructing generator object from puzzle file
        # (space delimited columns, line delimited rows)
        gen = Generator("base.txt")

        # applying 100 random transformations to puzzle
        gen.randomize(100)

        # applying logical reduction with corresponding difficulty cutoff
        gen.reduce_via_logical(self.difficulty[0])

        # catching zero case
        if self.difficulty[1] != 0:
            # applying random reduction with corresponding difficulty cutoff
            gen.reduce_via_random(self.difficulty[1])

        # getting copy after reductions are completed
        final = gen.board.copy()

        return final
