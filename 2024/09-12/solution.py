import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

import numpy as np
import argparse
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

# ------------------------------------------------------------------------------------------- #
#                                        <START>                                              #
# ------------------------------------------------------------------------------------------- #     
@timer(return_time=True)
def submission(p_input, profile=False):
    inp = list(map(int, list(load_input(p_input))))


    @timer(return_time=True)
    def task1(inp):
        """
        TASK 1
        """
        expanded = []
        for i, length in enumerate(map(int, inp)):
            expanded.extend([str(i // 2)] * length if i % 2 == 0 else ['.'] * length)

        leftmost_free = 0  
        for i in range(len(expanded)):
            if expanded[i] == '.':
                leftmost_free = i
                break

        for i in range(len(expanded) - 1, -1, -1):
            if expanded[i] != '.': 
                if leftmost_free < i:
                    expanded[leftmost_free], expanded[i] = expanded[i], '.'
                    for j in range(leftmost_free + 1, len(expanded)):
                        if expanded[j] == '.':
                            leftmost_free = j
                            break
        
        
        checksum = 0
        for pos, block in enumerate(expanded):
            if block != '.':
                checksum += pos * int(block)

        return checksum
        

    @timer(return_time=True)
    def task2(inp):
        """
        TASK 2
        """
        expanded = []
        for i, length in enumerate(map(int, inp)):
            expanded.extend([str(i // 2)] * length if i % 2 == 0 else ['.'] * length)

        file_ids = sorted(set(block for block in expanded if block != '.'), reverse=True)

        for file_id in file_ids:
            file_blocks = [i for i, block in enumerate(expanded) if block == file_id]
            file_size = len(file_blocks)

            free_start = None
            free_length = 0
            for i, block in enumerate(expanded):
                if block == '.':
                    if free_start is None:
                        free_start = i
                    free_length += 1
                    if free_length == file_size:
                        if free_start < file_blocks[0]:
                            for idx in file_blocks:
                                expanded[idx] = '.'  
                            for j in range(free_start, free_start + file_size):
                                expanded[j] = file_id 
                            break
                else:
                    free_start = None
                    free_length = 0

        checksum = 0
        for pos, block in enumerate(expanded):
            if block != '.':
                checksum += pos * int(block)

        return checksum
    
    if profile:
        result_task1, time_task1 = average_time(1000, task1, inp)
        result_task2, time_task2 = average_time(1000, task2, inp)
    else:
        result_task1, time_task1 = task1(inp)
        result_task2, time_task2 = task2(inp)


    return result_task1, time_task1, result_task2, time_task2
# ------------------------------------------------------------------------------------------- #
#                                         <END>                                               #
# ------------------------------------------------------------------------------------------- #


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def main():
    input_file = "example_input.txt"

    opt = get_args()
    if opt.submission:
        input_file = "input.txt"

    with profile(opt.submission) as results:
        (result_task1, time_task1, result_task2, time_task2), total_time = submission(input_file)
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