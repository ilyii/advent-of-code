import argparse
import os
import sys
import re
import math
from collections import defaultdict

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def calculate(data):
    symbols = {
        (i, j)
        for i, l in enumerate(data)
        for j, x in enumerate(l)
        if not x.isalnum() and not x == "." 
    }
    numbers = re.compile(r"(\d+)")

    symbol_numbers = defaultdict(list)
    for i, line in enumerate(data):
        for match in numbers.finditer(line):
            n = int(match.group(0))
            box = {
                (i + di, j + dj)
                for di in range(-1, 2)
                for dj in range(-1, 2)
                for j in range(match.start(), match.end())
            }
            for s in symbols & box:
                symbol_numbers[s].append(n)
    return symbol_numbers


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1 = sum(sum(v) for v in calculate(data.splitlines()).values())
        answer_2 = sum(math.prod(v) for v in calculate(data.splitlines()).values() if len(v) == 2)
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")

