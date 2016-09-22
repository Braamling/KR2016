"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
import random
import csv

import numpy as np

import matplotlib.pyplot as plt


def get_sudoku(csv_file):
    # Get the first sudoku and replace empty cells with 0's
    sudoku = csv_file.next()[0].replace(".", "0")

    # Convert the sudoku to an numpy array for reshaping and conver to int
    sudoku = np.asarray(list(sudoku)).astype(np.int)

    return sudoku.reshape(9, 9).tolist()


def plot_sudoku(results, no_region_first, no_region_average,
                shuffle_first, shuffle_average):
    plt.plot(results, 'b-', label='sudoku')
    plt.plot(no_region_first, 'r-', label='no regions, first')
    plt.plot(no_region_average, 'g-', label='no regions, average')
    plt.plot(shuffle_first, 'y-', label='no regions, average')
    plt.plot(shuffle_average, 'p-', label='no regions, average')
    plt.show()


if __name__ == '__main__':
    sudoku_results = []
    shuffle_avg = []
    shuffle_first = []
    no_region_avg = []
    no_region_first = []

    # Open csv file
    sudokus = csv.reader(open("input/sudoku_expert_100k.csv"), delimiter=",")

    # Open and initialize a csv file + writer.
    with open('results.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for x in xrange(0, 3000):
            print x

            sudoku = get_sudoku(sudokus)

            # Solve the Sudoku with a region rule applied
            res_normal = solver.solve(sudoku, with_region_rule=True)

            res_alt = solver.solve(sudoku, with_region_rule=False)

            # Shuffle the row's of the sudoku to create a regionless sudoku
            random.shuffle(sudoku)

            # Solve the shuffled sudoku
            res_shuf = solver.solve(sudoku, with_region_rule=False)

            # Append the sudoku results
            sudoku_results.append(res_normal[1])

            # Write line to csv
            csv_writer.writerow(res_normal + res_alt + res_shuf)

            # Append the sudoku results
            no_region_avg.append(res_alt[1])
            no_region_first.append(res_alt[2])
            shuffle_avg.append(res_shuf[1])
            shuffle_first.append(res_shuf[2])

    # Plot all the statistics of the sudoku solver
    plot_sudoku(sudoku_results, no_region_first,
                no_region_avg, shuffle_first, shuffle_avg)
