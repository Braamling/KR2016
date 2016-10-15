"""
The main script that generates sudokus with and without region rules
and solves these with pycosat
"""
import solver
import random
import csv
import copy

import numpy as np

import matplotlib.pyplot as plt


def get_sudoku(csv_file):
    # Get the first sudoku and replace empty cells with 0's
    sudoku = csv_file.next()[0].replace(".", "0")

    # Convert the sudoku to an numpy array for reshaping and conver to int
    sudoku = np.asarray(list(sudoku)).astype(np.int)

    return sudoku.reshape(9, 9).tolist()


def plot_sudoku(results, no_region_first,
                shuffle_first):
    plt.plot(results, 'b-', label='sudoku')
    plt.plot(no_region_first, 'r-', label='no regions, first')
    # plt.plot(no_region_average, 'g-', label='no regions, average')
    plt.plot(shuffle_first, 'y-', label='no regions, average')
    # plt.plot(shuffle_average, 'p-', label='no regions, average')
    plt.show()


def print_progress(x, y, n_sodukus, rewinds):
    print "\nIteration: " + str(y) + "/" + str(rewinds)
    print "Iteration: " + str(x) + "/" + str(n_sodukus)


if __name__ == '__main__':
    rewinds = 10
    n_sodukus = 3000

    sudoku_results = np.empty([n_sodukus, rewinds])
    shuffle_first = np.empty([n_sodukus, rewinds])
    no_region_first = np.empty([n_sodukus, rewinds])

    # Open csv file
    sudoku_file = open("input/sudoku_simple_100k.csv")
    sudokus = csv.reader(sudoku_file, delimiter=",")

    # Open and initialize a csv file + writer.
    with open('results.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Iterate over all sudoku's n times
        for y in xrange(0, rewinds):
            # Rewind sudoku file
            sudoku_file.seek(0)

            for x in xrange(0, n_sodukus):
                print_progress(x, y, n_sodukus, rewinds)

                # Set a seed in order to pseudo shuffle sudoku's
                random.seed(x * 3)
                sudoku = get_sudoku(sudokus)

                sudoku1 = copy.deepcopy(sudoku)
                sudoku2 = copy.deepcopy(sudoku)

                # Solve the Sudoku with a region rule applied
                res_normal = solver.solve(sudoku1, with_region_rule=True)
                res_alt = solver.solve(sudoku, with_region_rule=False)

                # Shuffle the row's of the sudoku to create a regionless sudoku
                random.shuffle(sudoku2)

                # Solve the shuffled sudoku
                res_shuf = solver.solve(sudoku2, with_region_rule=False)

                # Append the sudoku results
                # sudoku_results.append(res_normal)
                # no_region_first.append(res_alt)
                # shuffle_first.append(res_shuf)

                sudoku_results[x, y] = res_normal
                no_region_first[x, y] = res_alt
                shuffle_first[x, y] = res_shuf

        for normal, alt, shul in zip(sudoku_results, no_region_first,
                                     shuffle_first):
            csv_writer.writerow((normal.mean(), alt.mean(), shul.mean()))

    # Plot all the statistics of the sudoku solver
    plot_sudoku(sudoku_results, no_region_first, shuffle_first)
