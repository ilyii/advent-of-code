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
    def monotonic(L):
        return all(x<y for x, y in zip(L, L[1:])) or all(x>y for x, y in zip(L, L[1:]))

    
    def in_distance(L, max_dist):
        return all(abs(x-y) <= max_dist for x, y in zip(L, L[1:]))


    reports = [[int(x) for x in line.split()] for line in day_input.split("\n")]
    safe_reports = 0
    for report in reports:
        if monotonic(report) and in_distance(report, 3):
            safe_reports += 1

    return safe_reports


@timer(return_time=True)
def task2(day_input):
    def monotonic(L):
        return all(x<y for x, y in zip(L, L[1:])) or all(x>y for x, y in zip(L, L[1:]))
    
    def in_distance(L, max_dist):
        return all(abs(x-y) <= max_dist for x, y in zip(L, L[1:]))

    reports = [[int(x) for x in line.split()] for line in day_input.split("\n")]
    pseudo_reports = [list(combinations(r, len(r)-1)) for r in reports]
    safe_reports = 0
    for report_list in pseudo_reports:
        for report in report_list:
            if monotonic(report) and in_distance(report, 3):
                safe_reports += 1
                break
    
    return safe_reports


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

    if INPUT_FILE == "input.txt":
        # 1000 times and average the time
        avg_time_task1 = average_time(1000, task1, day_input)
        avg_time_task2 = average_time(1000, task2, day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()