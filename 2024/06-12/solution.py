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

from utils import average_time, load_input, timer, write_times_to_readme, timer_wrapper

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")

# ------------------------------------------------------------------------------------------- #
#                                        <START>                                              #
# ------------------------------------------------------------------------------------------- #     
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # UP, RIGHT, DOWN, LEFT


def is_out_of_bounds(grid, position):
    """Check if the position is outside the bounds of the grid."""
    rows, cols = len(grid), len(grid[0])
    x, y = position
    return x < 0 or x >= rows or y < 0 or y >= cols


def patrol_path(grid, obstacles, start_pos, start_dir):
    """
    Simulates the guard's patrol and yields positions and directions visited.
    """
    position = start_pos
    direction_index = start_dir

    while True:
        x, y = position
        dir_x, dir_y = DIRECTIONS[direction_index]
        blocked = False

        while not is_out_of_bounds(grid, (x, y)):
            if (x, y) in obstacles:
                blocked = True
                break
            yield (x, y), direction_index
            x += dir_x
            y += dir_y

        if not blocked:
            break  # Exits the patrol when out of bounds

        position = (x - dir_x, y - dir_y)  # Revert to the last valid position
        direction_index = (direction_index + 1) % 4  # Turn right

@timer(return_time=True)
def distinct_positions_visited(grid, obstacles, start_pos, start_dir):
    """
    Calculates the number of unique positions visited during the patrol.
    """
    visited = set((pos for pos, _ in patrol_path(grid, obstacles, start_pos, start_dir)))
    return len(visited)

@timer(return_time=True)
def find_loop_obstructions(grid, obstacles, start_pos, start_dir):
    """
    Identifies potential positions for adding an obstacle that creates a patrol loop.
    """
    visited = set(patrol_path(grid, obstacles, start_pos, start_dir))
    loop_candidates = set()

    for (pos, direction) in visited:
        x, y = pos
        dir_x, dir_y = DIRECTIONS[direction]
        potential_obstruction = (x + dir_x, y + dir_y)

        # Skip invalid positions for an obstruction
        if (
            is_out_of_bounds(grid, potential_obstruction)
            or potential_obstruction in obstacles
            or potential_obstruction == start_pos
        ):
            continue

        extended_obstacles = obstacles | {potential_obstruction}
        current_pos = start_pos
        current_dir = 0
        seen_states = set()

        while True:
            state = (current_pos, current_dir)
            if state in seen_states:
                # Loop detected; mark this obstruction as a valid candidate
                loop_candidates.add(potential_obstruction)
                break
            seen_states.add(state)

            x, y = current_pos
            dir_x, dir_y = DIRECTIONS[current_dir]
            next_pos = (x + dir_x, y + dir_y)

            if is_out_of_bounds(grid, next_pos):
                break

            if next_pos in extended_obstacles:
                current_dir = (current_dir + 1) % 4
            else:
                current_pos = next_pos

    return len(loop_candidates)


def submission(input_file, profile=False):
    grid = load_input(input_file).splitlines()
    grid = [list(row) for row in grid]  
    obstacles = {(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "#"}
    start_position = [(i,j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "^"][0]
    start_direction = 0  

    distinct_count, time1 = distinct_positions_visited(grid, obstacles, start_position, start_direction)

    loop_obstructions_count, time2 = find_loop_obstructions(grid, obstacles, start_position, start_direction)

    return (distinct_count, loop_obstructions_count), (time1, time2)

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
        res, times = submission(input_file)
        res1, res2 = res
        time1, time2 = times
        results["part1"] = res1
        results["part2"] = res2

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {res1}")
    print(f"Task 2: {res2}")

    # Print the times
    print("\nTimes:")
    print(f"Task 1: {time1:.6f} seconds")
    print(f"Task 2: {time2:.6f} seconds")

if __name__ == "__main__":
    main()