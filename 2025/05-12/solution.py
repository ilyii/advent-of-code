import argparse
import os
import sys

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def read(args):
    """Parse input - returns file content as string"""
    filepath = "input.txt" if args.submission else "example_input.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def read_lines(args):
    """Parse input - returns list of lines"""
    return read(args).split("\n")


def read_ints(args):
    """Parse input - returns list of integers"""
    return [int(x) for x in read_lines(args)]


def read_grid(args):
    """Parse input - returns 2D grid of characters"""
    return [list(line) for line in read_lines(args)]


def print_grid(grid):
    """Print 2D grid"""
    for row in grid:
        print("".join(row))

def printr(*results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

# ----------------------------------- #
# ----------- Custom Code ----------- #
# ----------------------------------- #

def solve(ranges, ids):
    """
    Idea: Sort and then apply binary search or two-pointer technique
    """

    # 
    ranges.sort(key=lambda x: x[0])
    ids.sort()


    # Part 1: Go left to right through each range and check ids
    part1 = 0
    for id_ in ids:
        for start, end in ranges:
            if start <= id_ <= end:
                part1 += 1
                break

    # Part 2: Count the total number of range ids covered (overlaps are to be resolved)
    part2 = 0

    cur_start, cur_end = ranges[0]
    for nxt_start, nxt_end in ranges[1:]:
        if nxt_start > cur_end:
            part2 += cur_end - cur_start + 1
            cur_start, cur_end = nxt_start, nxt_end
        else:
            cur_end = max(cur_end, nxt_end)

    part2 += cur_end - cur_start + 1

    
    return part1, part2
    

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)  # or read(opt), read_ints(opt), read_grid(opt)

    with profile(opt.submission) as results:
        result1 = 0
        result2 = 0

        # Solve both parts here
        ranges, ids = data.split("\n\n")
        ranges = [tuple(map(int, line.split("-"))) for line in ranges.split("\n")]
        ids = list(map(int, ids.split("\n")))

        result1, result2 = solve(ranges, ids)

        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
