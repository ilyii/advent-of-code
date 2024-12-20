import argparse
from itertools import combinations
import os

import numpy as np


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def read(args):
    """ Parse input """
    if args.submission:
        filepath = "input.txt"
    else:
        filepath = "example_input.txt"

    return open(filepath, "r", encoding="utf-8")


def printr(results):
    """ Print results """
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")

    print("--------------------")


# ---------------------------- #

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)
    grid = {i+j*1j: c for i,r in enumerate(data)
                for j,c in enumerate(r) if c not in "#\n"}
    
    start = next(k for k,v in grid.items() if v == "S")
    
    dist = {start: 0}
    
    stack = [start]
    while stack:
        pos = stack.pop()
        for new in pos-1, pos+1, pos-1j, pos+1j:
            if new in grid and new not in dist:
                dist[new] = dist[pos] + 1
                stack.append(new)

    print(f"Initial path length: {dist[next(k for k,v in grid.items() if v == 'E')]}")
    
    part_1 = part_2 = 0

    for (p,i), (q,j) in combinations(dist.items(), 2):
        d = abs((p-q).real) + abs((p-q).imag)
        if d == 2 and j-i-d >= 100: part_1 += 1
        if d < 21 and j-i-d >= 100: part_2 += 1

    printr([part_1, part_2])

