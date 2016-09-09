"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
import random
import time

import matplotlib.pyplot as plt

from pprint import pprint
from sudoku_generator import SudokuGenerator


if __name__ == '__main__':
    sudoku_results = []
    no_region_results = []

    # Create a Sudoku generator instance for medium difficult sudokus.
    generator = SudokuGenerator('medium')

    # Take computational start time
    start_normal = time.time()
    for x in xrange(0, 10000):
        # Generate a medium difficult sudoku and convert to an array
        sudoku = generator.get_sudoku().get_array()

        # Solve the Sudoku with a region rule applied
        solver.solve(sudoku, with_region_rule=True)

        # Shuffle the row's of the sudoku to create a regionless sudoku
        random.shuffle(sudoku)

        # Solve the shuffled sudoku
        solver.solve(sudoku, with_region_rule=False)

    # Print the sudoku solution.
    pprint(sudoku)
