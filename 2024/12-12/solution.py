import argparse
import os
from collections import defaultdict, deque

import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRECTION_NAMES = ["R", "D", "L", "U"]

def submission(data):
    # grid walk: every square has a perimeter of 4 - num neighbors it has (when checking border, perimeter is true)

    visited = set()
    n,m = data.shape
    total_perimeter = 0
    
    fields = list()
    total_sides = 0
    outer_pos = list()
    while len(visited) < n*m:
        for x in range(n):
            for y in range(m):
                if (x,y) not in visited:
                    char = data[x, y]
                    perimeter = 0
                    num_elems = 0
                    stack = [(x,y)]
                    field = set()
                    outpos = set()
                    while stack:
                        nx,ny = stack.pop()
                        if (nx,ny) in visited:
                            continue
                        field.add((nx,ny))
                        visited.add((nx,ny))

                        num_elems += 1
                        for idx, (dx,dy) in enumerate(DIRECTIONS):
                            if nx+dx < 0 or nx+dx >= n or ny+dy < 0 or ny+dy >= m:
                                perimeter += 1
                                outpos.add((nx,ny, dx,dy))
            
                            elif data[nx+dx, ny+dy] != char:
                                perimeter += 1
                                outpos.add((nx,ny, dx,dy))
                            else:

                                stack.append((nx+dx, ny+dy))

                                
                    fields.append(field)
                    outer_pos.append(list(outpos))

                    total_perimeter += num_elems*perimeter
    
    for outpos in outer_pos:
        if outpos[2] == 0:
            total_sides += 1
        elif outpos[2] == 1:
            total_sides += 1
        elif outpos[2] == 2:
            total_sides += 1
        elif outpos[2] == 3:
            total_sides += 1
    
 

    return total_perimeter, total_sides



def main():
    inputpath = "example_input.txt"

    opt = get_args()
    if opt.submission:
        inputpath = "input.txt"

    with open(inputpath, "r") as file:
        data = file.read().splitlines()
    data = np.array([np.array(list(line)) for line in data])
    print(data)
    
    
    result1, result2  = submission(data)

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()