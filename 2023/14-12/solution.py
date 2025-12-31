import argparse
from collections import defaultdict
import os
import re
import sys

import numpy as np

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--submission", action="store_true", help="Use real input for submission"
    )
    return parser.parse_args()


def read(args):
    """Parse input"""
    if args.submission:
        filepath = "input.txt"
    else:
        filepath = "example_input.txt"

    return open(filepath, "r", encoding="utf-8")


def printr(results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")

    print("--------------------")


if __name__ == "__main__":
    opt = get_args()
    data = read(opt).read().replace("\n", " ")
    # 1. Transpose
    # 2. Replace switch "." and "O"
    # 3. Count distances to right bound.
    def tilt(b):
        """ Implements a 90"""
        return " ".join(map("".join, zip(*(b.split())[::-1])))

    def count(b):
        return sum(i for r in b.split() for i, c in enumerate(r[::-1], 1) if c == "O")

    def roll(d):
        return re.sub("[.O]+", lambda m: "".join(sorted(m[0])[::-1]), tilt(d))
    
    with profile(opt.submission) as results:
        part_1 = count(roll(roll(roll(roll(data)))))
        

        def spinner(data, n, cache={}):
            for r in range(n):
                data = roll(roll(roll(roll(data))))
                if s:=cache.get(data,0): return cache[ (n-s) % (r-s) + (s-1) ]
                cache |= {data:r, r:count(tilt(data))}
        
        part_2 = spinner(data,1_000_000_000)
        results["part1"] = part_1
        results["part2"] = part_2
    
    printr([part_1, part_2])