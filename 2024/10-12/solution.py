import argparse
import os
from collections import defaultdict, deque

import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def get_neighbors(x, y, rows, cols):
    """Get valid neighbors."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            yield nx, ny

def count_distinct_trails(grid, start):
    rows, cols = len(grid), len(grid[0])
    
    trails = set()
    stack = [(start, [start])]

    while stack:
        (x, y), path = stack.pop()
        
        for nx, ny in get_neighbors(x, y, rows, cols):
            if (nx, ny) in path: continue  # Skip
            if grid[nx][ny] == grid[x][y] + 1:
                new_path = path + [(nx, ny)]
                if grid[nx][ny] == 9:
                    trails.add(tuple(new_path))
                else:
                    stack.append(((nx, ny), new_path))

    
    return trails


def submission(data):
    rows, cols = len(data), len(data[0]) 
    trailscore = set()
    rating = 0

    for x in range(rows):
        for y in range(cols):
            if data[x][y] == 0:
                trails = count_distinct_trails(data, (x, y))
                for trail in trails:
                    trailscore.add((trail[0], trail[-1]))
                rating += len(trails)

    return len(trailscore), rating  





def main():
    inputpath = "example_input.txt"

    opt = get_args()
    if opt.submission:
        inputpath = "input.txt"

    with open(inputpath, "r") as file:
        data = file.read().splitlines()
    data = np.array([np.array(list(map(int,list(line)))) for line in data])
    
    result1, result2  = submission(data)

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()