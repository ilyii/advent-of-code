import argparse
import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

import numpy as np
from tqdm import tqdm

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(par_dir))
from profiler import profile

from utils import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


@timer(return_time=True)
def task1(day_input):
    SPLITTER = "   " #\t ?
    left, right = zip(*[(int(s[0]), int(s[1])) for s in [x.split(SPLITTER) for x in day_input.split("\n")]])
    left = sorted([x for x in left])
    right = sorted([x for x in right])
    distances = [abs(x - y) for x, y in zip(left, right)]
    return sum(distances)


@timer(return_time=True)
def task2(day_input):
    SPLITTER = "   " #\t ?
    left, right = zip(*[(int(s[0]), int(s[1])) for s in [x.split(SPLITTER) for x in day_input.split("\n")]])
    right = Counter(right)
    score = sum(l*right[l] for l in left)
    return score


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def main():
    opt = get_args()
    INPUT_FILE = "input.txt" if opt.submission else "example_input.txt"
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, INPUT_FILE))

    with profile(opt.submission) as results:
        # Call the tasks and store their results (if needed)
        result_task1, time_task1 = task1(day_input)
        result_task2, time_task2 = task2(day_input)
        results["part1"] = result_task1
        results["part2"] = result_task2

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")


if __name__ == "__main__":
    main()