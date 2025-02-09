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
#                                                                                             #
# ------------------------------------------------------------------------------------------- #     
@timer(return_time=True)
def submission(p_input, profile=False):
    inp = load_input(os.path.join(cur_dir, p_input))

    @timer(return_time=True)
    def task1(day_input):
        rules, schedules = day_input.split("\n\n")
        rules = [list(map(int, rule.split("|"))) for rule in rules.split("\n")]
        schedules = [list(map(int, s.split(","))) for s in schedules.split("\n")]
        # print(rules)
        # print(schedules)
        score = 0
        for schedule in schedules:
            for idx, elem in enumerate(schedule):
                # In all rules, elem must be schedule[0] where a subsequent elem is schedule[1]
                if any([s,elem] in rules for s in schedule[idx+1:]):
                    # print(schedule)
                    break
            else:
                score += schedule[len(schedule)//2]
        
        return score


    @timer(return_time=True)
    def task2(day_input):
        rules, schedules = day_input.split("\n\n")
        rules = [list(map(int, rule.split("|"))) for rule in rules.split("\n")]
        schedules = [list(map(int, s.split(","))) for s in schedules.split("\n")]
        def reorder_schedule(schedule, rules):
            # Bubble sort according to the rules
            for i in range(len(schedule)):
                for j in range(i+1, len(schedule)):
                    if [schedule[i], schedule[j]] in rules:
                        schedule[i], schedule[j] = schedule[j], schedule[i]
            return schedule[len(schedule)//2]

        score = 0
        for schedule in schedules:
            for idx, elem in enumerate(schedule):
                if any([s,elem] in rules for s in schedule[idx+1:]):
                    score += reorder_schedule(schedule, rules)
                    break

            
        return score

    
    if profile:
        result_task1, time_task1 = average_time(1000, task1, inp)
        result_task2, time_task2 = average_time(1000, task2, inp)
    else:
        result_task1, time_task1 = task1(inp)
        result_task2, time_task2 = task2(inp)

    
    return result_task1, time_task1, result_task2, time_task2
# ------------------------------------------------------------------------------------------- #
#                                                                                             #
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