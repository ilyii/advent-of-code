import argparse
import os
import sys
import time
import re
import math

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def part1(data):
    times, distances = map(lambda x: list(map(int, re.findall(r'\d+', x))), data.splitlines())
    prod = []
    for t, d in zip(times, distances):
        prod.append(sum([((t-x)*x) > d for x in range(t+1)]))
    return math.prod(prod)


def part2(data):
    t,d = [int("".join(re.findall(r'\d+', l))) for l in data.splitlines()]
    lower_bound = next(x for x in range(t + 1) if (t - x) * x > d)
    upper_bound = next(x for x in reversed(range(t + 1)) if (t - x) * x > d)

    return upper_bound - lower_bound + 1

    



if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1 = part1(data)
        answer_2 = part2(data)
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
