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

from util import average_time, load_input, timer, write_times_to_readme

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
    ADV_PATTERN = r"do\(\).*?(mul\((\d+),(\d+)\))"
    BEGIN_PATTERN = r"(mul\((\d+),(\d+)\))+.*?don't\(\)"
    mults_1 = re.findall(BEGIN_PATTERN, day_input)
    print(mults_1)
    mults_2 = re.findall(ADV_PATTERN, day_input)
    score = sum(int(a) * int(b) for a, b in mults_1) + sum(int(a) * int(b) for a, b in mults_2)
    return score



def main():
    INPUT_FILE = "input.txt"
    # INPUT_FILE = "example_input.txt"
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, INPUT_FILE))

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # if INPUT_FILE == "input.txt":
    #     # 1000 times and average the time
    #     avg_time_task1 = average_time(1000, task1, day_input)
    #     avg_time_task2 = average_time(1000, task2, day_input)
    #     print("\nAverage times:")
    #     print(f"Task 1: {avg_time_task1:.6f} seconds")
    #     print(f"Task 2: {avg_time_task2:.6f} seconds")
    #     write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()