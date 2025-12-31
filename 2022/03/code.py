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
    data = [e.replace("\n","") for e in inp.readlines()]
    #print(data)
    summation = 0
    for line in data:
        if len(line) < 1:
            continue
        half1 = set(line[:int(len(line)/2)])
        half2 = set(line[int(len(line)/2):])
        #print(half1, half2)
        char = list(half1.intersection(half2))

        char = list(half1.intersection(half2))[0]

        summation += ord(char)-38 if 65 <= ord(char) <= 90 else ord(char)-96
    # part 1
    part1 = summation
    # part 2
    summation = 0
    for i in range(100):
        f,s,t = set(data[i*3]),set(data[i*3+1]), set(data[i*3+2])
        #print(f,s,t)
        i1 = f.intersection(s)
        char = list(i1.intersection(t))[0]
        summation += ord(char) - 38 if 65 <= ord(char) <= 90 else ord(char) - 96
    part2 = summation
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