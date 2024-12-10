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

from utils import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


@timer(return_time=True)
def task1(day_input):
    
    grid = day_input.split("\n")
    rows = len(grid)
    cols = len(grid[0])
    
    directions = [
        (0, 1),   
        (0, -1),  
        (1, 0),   
        (-1, 0),  
        (1, 1),  
        (1, -1), 
        (-1, 1), 
        (-1, -1) 
    ]
    
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "X":                
                for dr, dc in directions:
                     if (
                        0 <= r + dr < rows and
                        0 <= c + dc < cols and
                        0 <= r + 2*dr < rows and
                        0 <= c + 2*dc < cols and
                        0 <= r + 3*dr < rows and
                        0 <= c + 3*dc < cols
                    ):
                        if (
                            grid[r + dr][c + dc] == "M" and
                            grid[r + 2*dr][c + 2*dc] == "A" and
                            grid[r + 3*dr][c + 3*dc] == "S"
                        ):
                            count += 1
        
    return count


@timer(return_time=True)
def task2(day_input):
    grid = day_input.split("\n")
    rows = len(grid)
    cols = len(grid[0])
    
    directions = [
        (1, 1),  
        (-1, -1) 
    ]
    
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "A":                
                for dr, dc in directions:
                     if (
                        0 <= r + dr < rows and
                        0 <= c + dc < cols and
                        0 <= r - dr < rows and
                        0 <= c - dc < cols
                    ):
                        if (
                            (grid[r + dr][c + dc] == "M" and
                            grid[r - dr][c - dc] == "S") and
                            (
                                (grid[r - dr][c + dc] == "M" and
                            grid[r + dr][c - dc] == "S")
                              or
                            (grid[r - dr][c + dc] == "S" and
                            grid[r + dr][c - dc] == "M")
                            )

                        ):
                            count += 1
        
    return count


def main():
    INPUT_FILE = "input.txt"
    # INPUT_FILE = "example_input_2.txt"
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