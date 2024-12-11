import argparse
import os
from collections import defaultdict, deque

import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def submission(data):
    return 0,0


def main():
    inputpath = "example_input.txt"

    opt = get_args()
    if opt.submission:
        inputpath = "input.txt"

    with open(inputpath, "r") as file:
        data = file.read().splitlines()
    
    
    result1, result2  = submission(data)

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()