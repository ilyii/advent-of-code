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
    inp = load_input(p_input)
    unique_chars = set(inp)
    unique_chars.remove("\n")
    unique_chars.remove(".")
    unique_chars = list(unique_chars)
    inp = [list(line) for line in inp.splitlines()]

    def is_within_bounds(pos):
        x, y = pos
        return 0 <= x < len(inp) and 0 <= y < len(inp[x])

    
    def print_grid(grid, nodes):
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if (x, y) in nodes:
                    print("#", end="")
                else:
                    print(grid[x][y], end="")
            print()
        print()

    

    @timer(return_time=True)
    def task1(inp):
        """
        TASK 1
        """
        nodes = set()
        for symb in unique_chars:
            positions = [(x, y) for x in range(len(inp)) for y in range(len(inp[x])) if inp[x][y] == symb]

            combs = combinations(positions, 2)
            for pos1, pos2 in combs:
                x1, y1 = pos1
                x2, y2 = pos2
                x_dist = x1 - x2
                y_dist = y1 - y2
                # Extend the line between the two points 
                smaller_node = (x1 + x_dist, y1 + y_dist)
                larger_node = (x2 - x_dist, y2 - y_dist)

                if is_within_bounds(smaller_node) and smaller_node not in positions:
                    nodes.add(smaller_node)
                if is_within_bounds(larger_node) and larger_node not in positions:
                    nodes.add(larger_node)

        return len(nodes)
                        
            
        



    @timer(return_time=True)
    def task2(inp):
        """
        TASK 2
        """
        nodes_extended = set()
        for symb in unique_chars:
            positions = [(x, y) for x in range(len(inp)) for y in range(len(inp[x])) if inp[x][y] == symb]
            nodes_extended.update(positions)

            combs = combinations(positions, 2)
            for pos1, pos2 in combs:
                x1, y1 = pos1
                x2, y2 = pos2
                x_dist = x1 - x2
                y_dist = y1 - y2

                smaller_node = (x1 + x_dist, y1 + y_dist)
                while is_within_bounds(smaller_node):
                    if inp[smaller_node[0]][smaller_node[1]] == ".":                        
                        nodes_extended.add(smaller_node)
                    smaller_node = (smaller_node[0] + x_dist, smaller_node[1] + y_dist)
                    

                larger_node = (x2 - x_dist, y2 - y_dist)
                while is_within_bounds(larger_node):
                    if inp[larger_node[0]][larger_node[1]] == ".":                        
                        nodes_extended.add(larger_node)
                    larger_node = (larger_node[0] - x_dist, larger_node[1] - y_dist)
                
                
        return len(nodes_extended) 
    
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