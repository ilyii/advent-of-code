import argparse
import os
import sys
from collections import defaultdict, deque
from itertools import combinations

import numpy as np

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def identify_empty_rows_and_cols(grid):
    """Identify empty rows and columns."""
    empty_rows = {i for i in range(len(grid)) if '#' not in grid[i]}
    empty_cols = {j for j in range(len(grid[0])) if all(row[j] != '#' for row in grid)}
    return empty_rows, empty_cols

def dist_with_expansion(start, end, empty_rows, empty_cols, expansion_multiplier):
    """Calculate adjusted distance considering expanded empty rows/cols."""
    start_x, start_y = start
    end_x, end_y = end

    # Base Manhattan distance
    x_dist = abs(start_x - end_x)
    y_dist = abs(start_y - end_y)

    # Add expansion multiplier for each unique empty row crossed
    x_empty_count = sum(1 for x in range(min(start_x, end_x) + 1, max(start_x, end_x)) if x in empty_rows)
    y_empty_count = sum(1 for y in range(min(start_y, end_y) + 1, max(start_y, end_y)) if y in empty_cols)

    x_dist += x_empty_count * (expansion_multiplier - 1)
    y_dist += y_empty_count * (expansion_multiplier - 1)

    return x_dist + y_dist

def submission(data):
    """Calculate the total distance for expanded universe."""
    galaxies = [(x, y) for x in range(len(data)) for y in range(len(data[0])) if data[x][y] == "#"]
    empty_rows, empty_cols = identify_empty_rows_and_cols(data)
    part1 = 0
    part2 = 0
    for (g1, g2) in combinations(galaxies, 2):
        part1 += dist_with_expansion(g1, g2, empty_rows, empty_cols, 2)
        part2 += dist_with_expansion(g1, g2, empty_rows, empty_cols, 1000000)

    return part1, part2



def main():
    inputpath = "example_input.txt"

    opt = get_args()
    if opt.submission:
        inputpath = "input.txt"

    with open(inputpath, "r") as file:
        data = file.read().splitlines()
    data = [list(line) for line in data]

    with profile(opt.submission) as results:
        result1, result2 = submission(data)
        results["part1"] = result1
        results["part2"] = result2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()