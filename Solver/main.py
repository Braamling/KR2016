"""
The main script that generates sudokus with and without region rules and solves these with pycosat
"""
import solver
import generator


if __name__ == '__main__':
    new_sudoku_example = generator.generate() # change this later to a loop
    solver.solve(new_sudoku_example)
