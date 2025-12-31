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


def solution(inp):
    # part 1
    data = [e.replace("\n","")for e in inp.readlines()]
    #print(data)
    elves_calories = []
    current = 0
    for elem in data:
        if elem == "":
            elves_calories.append(current)
            current = 0
        else:
            current += int(elem)

    part1 = max(elves_calories)
    # part 2
    elves_calories.sort(reverse=True)
    part2 = elves_calories[0]+elves_calories[1]+elves_calories[2]
    return part1, part2


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with profile(opt.submission) as results:
        data = open(inputpath)
        result1, result2 = solution(data)
        results["part1"] = result1
        results["part2"] = result2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
