import argparse
from itertools import combinations
import os
import sys

import numpy as np

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


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


def str2bool(grid):
    """ Convert string to boolean """
    return np.array([[x == "#" for x in row] for row in grid.split("\n")])
if __name__ == "__main__":
    opt = get_args()
    data = read(opt).read()
    schemes = data.split("\n\n")

    keys = []
    locks = []
    for scheme in schemes:
        if any(x == "." for x in scheme.split()[0]):
            keys.append(str2bool(scheme))
        else:
            locks.append(str2bool(scheme))
    
    with profile(opt.submission) as results:
        part_1 = 0
        for lock in locks:
            for key in keys:
                if not np.any(np.logical_and(lock, key)):
                    part_1 += 1
        
        results["part1"] = part_1
        results["part2"] = None

    printr([part_1])