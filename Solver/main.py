"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
import random
from pprint import pprint
from sudoku_generator import SudokuGenerator


if __name__ == '__main__':
    # Create a Sudoku generator instance for medium difficult sudokus.
    generator = SudokuGenerator('hard')

    # Generate a medium difficult sudoku and convert to an array
    sudoku = generator.get_sudoku().get_array()

    # Shuffle the row's of the sudoku to create a regionless sudoku
    random.shuffle(sudoku)

    # Solve the Sudoku
    solver.solve(sudoku)

    # Print the sudoku solution.
    pprint(sudoku)
