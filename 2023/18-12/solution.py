import argparse
from collections import defaultdict, deque
import os
import sys
from numbers import Number
from typing import Any, Tuple

import numpy as np

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

D = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}
def submission(directions, distances, colors) -> Tuple[Number, Number]:
    """ Logic """
    start = (0,0)
    hull = set()
    pos = start
    for idx, direction in enumerate(directions):
        dist = distances[idx]
        dx, dy = D[direction]
        for i in range(dist+1):
            pos = (pos[0]+dx*i, pos[1]+dy*i)
            hull.add(pos)

    
    min_x = min(hull, key=lambda x: x[0])[0]
    min_y = min(hull, key=lambda x: x[1])[1]
    # Shift to positive
    hull = {(x+abs(min_x), y+abs(min_y)) for x, y in hull}
    max_x = max(hull, key=lambda x: x[0])[0]
    max_y = max(hull, key=lambda x: x[1])[1]
    print(hull)
    grid = np.array([["." for _ in range(max_x+1)] for _ in range(max_y+1)])
    for x, y in hull:
        grid[y][x] = "#"

    print(grid)
    import matplotlib.pyplot as plt
    def convert2img(grid):
        img = np.zeros((grid.shape[0], grid.shape[1], 3)).astype(np.uint8)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i][j] == "#":
                    img[i][j] = 0
                else:
                    img[i][j] = 255
        return img
    plt.imshow(convert2img(grid))
    plt.show()


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read().splitlines()
    directions, distances, colors = zip(*[line.split() for line in data])    
    directions = list(directions)
    distances = list(map(int, distances))
    colors = [color.rstrip(")").lstrip("(") for color in colors]
    # ---- SUBMISSION ---- #
    with profile(opt.submission) as results:
        result1, result2 = submission(directions, distances, colors)
        results["part1"] = result1
        results["part2"] = result2

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")