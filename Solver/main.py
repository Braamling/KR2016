"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
import random
import csv
import numpy as np

import matplotlib.pyplot as plt

from pprint import pprint
from sudoku_generator import SudokuGenerator


def get_sudoku(csv_file):
    # Get the first sudoku and replace empty cells with 0's
    sudoku = csv_file.next()[0].replace(".", "0")

    # Convert the sudoku to an numpy array for reshaping and conver to int
    sudoku = np.asarray(list(sudoku)).astype(np.int)
    print sudoku.reshape(9, 9)
    return sudoku.reshape(9, 9).tolist()


if __name__ == '__main__':
    sudoku_results = []
    no_region_results = []

    # Create a Sudoku generator instance for medium difficult sudokus.
    generator = SudokuGenerator('medium')

    # Open csv file
    sudokus = csv.reader(open("input/sudoku_expert_100k.csv"), delimiter=",")

    # Open and initialize a csv file + writer.
    with open('results.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for x in xrange(0, 100):
            sudoku = get_sudoku(sudokus)
            print sudoku
            # Generate a medium difficult sudoku and convert to an array
            # sudoku = generator.get_sudoku().get_array()

            # Solve the Sudoku with a region rule applied
            res_normal = solver.solve(sudoku, with_region_rule=True)

            # Shuffle the row's of the sudoku to create a regionless sudoku
            random.shuffle(sudoku)

            print "solver1"
            # Solve the shuffled sudoku
            res_alt = solver.solve(sudoku, with_region_rule=True)
            print "solver"

            # Append the sudoku results
            sudoku_results.append(res_normal[1])

            # Write line to csv
            csv_writer.writerow(res_normal + res_alt)

            # Append the sudoku results
            no_region_results.append(res_alt[1])

    plt.plot(sudoku_results, 'b-', label='sudoku')
    plt.plot(no_region_results, 'r-', label='no regions')
    plt.show()
    # Print the sudoku solution.
    pprint(sudoku)
