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


CONSTRAINTS = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def count(data):
    sum = 0
    power = 0
    for line in data.splitlines():
        id = re.findall(r'(\w+)\s+(\d+)', line)[0][1]
        rgb = re.findall(r'(\d+)\s+(\w+)', line)
        max = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for m in rgb:
            count, color = m
            count = int(count)        
            if count > CONSTRAINTS[color]:            
                break
        else:
            sum += int(id)

        for m in rgb:
            count, color = m
            count = int(count)
            if max[color] < count:
                max[color] = count      
        power += max['red']*max['green']*max['blue']

    return sum, power


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1, answer_2 = count(data)
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")

