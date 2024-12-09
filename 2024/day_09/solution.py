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

    def parse(inp):
        id_counter = 0
        new_inp = ""
        for idx, elem in enumerate(inp):
            if idx % 2 == 0:
                new_inp += elem*f"{id_counter}"
                id_counter+=1
            else:
                new_inp += elem*f"."
            
            
        return list(new_inp)

    def compress(inp):
        # use the last digit and replace it with the first "." found
        for idx, elem in enumerate(inp):
            if elem == ".":
                if not any([x.isdigit() for x in inp[idx:]]):
                    break
                for idx2, elem in enumerate(reversed(inp)):                    
                    if elem.isdigit():
                        inp[idx] = elem
                        inp[len(inp)-idx2-1] = "."
                        break

        return inp
                        



    @timer(return_time=True)
    def task1(inp):
        """
        TASK 1
        """
        # 1. Parse input
        # 2. Compact
        # 3. Checksum
        new_inp = parse(inp)
        compressed = compress(new_inp)
        checksum = sum(idx*int(elem) for idx, elem in enumerate(compressed) if elem.isdigit())
        return checksum
        

    @timer(return_time=True)
    def task2(inp):
        """
        TASK 2
        """
        # Day-specific code for Task 2
        pass
    
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

    (result_task1, time_task1, result_task2, time_task2), total_time = submission(input_file)
    


    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    if opt.submission:
        # 1000 times and average the time
        avg_time_task1 = submission(input_file, profile=True)[1]
        avg_time_task2 = submission(input_file, profile=True)[3]
        avg_total_time = submission(input_file, profile=True)[4]

        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        print(f"Total time: {avg_total_time:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()