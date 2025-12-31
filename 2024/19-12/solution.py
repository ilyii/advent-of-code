import argparse
from functools import cache
import os
import sys
from numbers import Number
from typing import Any, Tuple

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def submission(towels: list, designs: list) -> Tuple[Number, Number]:
    """ Logic """
    
    @cache
    def match(d):
        nonlocal towels
        if d == "": 
            return 1
        return sum(match(d.removeprefix(t)) for t in towels.split(", ")
                   if d.startswith(t))


    part_1 =  sum(map(bool, map(match, designs)))
    part_2 = sum(map(int, map(match, designs)))
    return part_1, part_2



if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read()
    
    towels, designs = data.split("\n\n")
    designs = designs.splitlines()
    
    # ---- SUBMISSION ---- #
    with profile(opt.submission) as results:
        result1, result2 = submission(towels, designs)
        results["part1"] = result1
        results["part2"] = result2

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")