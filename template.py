import argparse
import os
import sys

# Add repo root for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def read(submission=False):
    """Read input file"""
    path = "input.txt" if submission else "example_input.txt"
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def solve(data):
    """Solve both parts - modify this!"""
    lines = data.splitlines()
    
    part1 = None
    part2 = None
    
    return part1, part2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input")
    args = parser.parse_args()
    
    data = read(args.submission)
    
    with profile(args.submission) as results:
        p1, p2 = solve(data)
        results["part1"] = p1
        results["part2"] = p2
    
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
