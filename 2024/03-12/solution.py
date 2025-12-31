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
    PATTERN = r"mul\((\d+),(\d+)\)"
    mults = re.findall(PATTERN, day_input)
    score = sum(int(a) * int(b) for a, b in mults)
    return score


@timer(return_time=True)
def task2(day_input):
    PATTERN = r"mul\((\d+),(\d+)\)" 
    ENABLE_PATTERN = r"do\(\)" 
    DISABLE_PATTERN = r"don't\(\)"    

    enabled = True
    score = 0

    for match in re.finditer(rf"{PATTERN}|{ENABLE_PATTERN}|{DISABLE_PATTERN}", day_input):
        instruction = match.group(0)
        
        if re.match(ENABLE_PATTERN, instruction):
            enabled = True
        elif re.match(DISABLE_PATTERN, instruction):
            enabled = False
        elif re.match(PATTERN, instruction) and enabled:
            x, y = map(int, re.findall(r"\d+", instruction))
            score += x * y

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