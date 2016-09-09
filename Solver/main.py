"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
from pprint import pprint
from sudoku_generator import SudokuGenerator


if __name__ == '__main__':
    generator = SudokuGenerator('medium')

    print generator.get_sudoku()

    hard = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 3, 0, 0, 0],
            [0, 7, 0, 0, 8, 0, 0, 0, 4],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]
    solver.solve(hard)
    pprint(hard)
