import argparse
import os
from numbers import Number
from typing import Any, Tuple

import numpy as np



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def column_equal(grid:np.ndarray, col:int) -> bool:
    return all(grid[:,col] == grid[0,col])

def submission(data:Any) -> Tuple[Number, Number]:
    """ Logic """

    def convert_to_int(grid_line):
        grid_line = ''.join(grid_line).replace('.', '0').replace('#', '1')
        return int(grid_line, 2)

    def check(grid, errors=0) -> int:
        grid = np.array([convert_to_int(x) for x in grid])
        for i in range(1, len(grid)):
            left = grid[:i][::-1]
            right = grid[i:]

            length = min(len(left), len(right))
            left = left[:length]
            right = right[:length]

            diff = [l ^ r for l, r in zip(left, right) if l != r]
            if len(diff) == errors:
                if errors == 0:
                    return i
                elif errors > 0:
                    if (diff[0] & (diff[0]-1) == 0) and diff[0] != 0:
                        return i

        return -1
    
    total_0 = 0
    total_1 = 0
    for grid in data:
        rows = check(grid, 0)
        cols = check(np.transpose(grid), 0)
        total_0 += rows * 100 if rows != -1 else 0
        total_0 += cols if cols != -1 else 0

        rows = check(grid, 1)
        cols = check(np.transpose(grid), 1)
        total_1 += rows * 100 if rows != -1 else 0
        total_1 += cols if cols != -1 else 0


    return total_0, total_1



if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read()

    data = data.split("\n\n")
    data = [np.array([list(x) for x in d.splitlines()]) for d in data]
    
    # ---- SUBMISSION ---- #
    result1, result2 = submission(data)

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

    if opt.submission:
        import timeit
        res = timeit.timeit(lambda: submission(data), number=10)
        print(f"Time: {res/10:.7f}s")