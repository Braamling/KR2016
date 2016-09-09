"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
from pprint import pprint
from sudoku_generator import SudokuGenerator


if __name__ == '__main__':
    generator = SudokuGenerator('medium')

    sudoku = generator.get_sudoku().get_array()

    pprint(sudoku)

    solver.solve(sudoku)
    pprint(sudoku)
