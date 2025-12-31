import argparse
import os
import sys
import time

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def calculate(X, p2=False):
    if all(x==0 for x in X):
        return 0
    D = []
    for i in range(len(X)-1):
        D.append(X[i+1]-X[i])
    
    if p2:
        return X[0] + (-1)*calculate(D,p2=True)
    return X[-1] + calculate(D)


def manage(data, p2=False):
    data = [[int(x) for x in row.split()] for row in data.splitlines()]
    return sum([calculate(row, p2) for row in data])



if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1 = manage(data)
        answer_2 = manage(data, True)
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
