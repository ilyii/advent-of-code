import argparse
import os
import sys
import re

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def calculate(data):
    sum = 0
    for l in data.splitlines():
        numbers = re.findall(r"\d", l)
        sum += int(f'{numbers[0]}{numbers[-1]}')
    return sum


if __name__ == "__main__":
    opt = get_args()
    inputpath = 'input.txt' if opt.submission else 'example_input.txt'
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1 = calculate(data)

        data = (
            data.replace("one", "o1e")
            .replace("two", "t2o")
            .replace("three", "t3e")
            .replace("four", "f4r")
            .replace("five", "f5e")
            .replace("six", "s6x")
            .replace("seven", "s7n")
            .replace("eight", "e8t")
            .replace("nine", "n9e")
        )
        answer_2 = calculate(data)
        
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")


