import argparse
from collections import Counter, defaultdict
from functools import cache
from itertools import pairwise
import os
import sys

import numpy as np

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--submission", action="store_true", 
        help="Use input.txt for submission"
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


def f(s:int) -> int:
    """ Pseudo-random number"""
    s ^= s << 6 & 0xFFFFFF
    s ^= s >> 5 & 0xFFFFFF
    return s ^ s << 11 & 0xFFFFFF


if __name__ == "__main__":
    opt = get_args()
    data = read(opt)

    with profile(opt.submission) as results:
        part_1 = 0
        part_2 = Counter()
        last_nums = []
        for s in (map(int, data)):
            nums = [s] + [s := f(s) for _ in range(2000)]
            part_1 += nums[-1]

            diffs = [b%10-a%10 for a,b in pairwise(nums)]

            seen = set()
            for i in range(len(nums)-4):
                seq = tuple(diffs[i:i+4])
                if seq not in seen:
                    seen.add(seq)
                    part_2[seq] += nums[i+4]%10
        
        results["part1"] = part_1
        results["part2"] = max(part_2.values())

    printr([part_1, max(part_2.values())])
