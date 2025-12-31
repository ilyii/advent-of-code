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


def solution(data):
    start_packet_position = None
    start_message_position = None
    
    for i, c in enumerate(data):
        i += 3
        chars = set({data[i], data[i - 1], data[i - 2], data[i - 3]})
        if len(chars) == 4:
            start_packet_position = i+1
            break

    for i, c in enumerate(data):
        i += 13
        chars = set(data[i-z] for z in range(14))
        if len(chars) == 14:
            start_message_position = i + 1
            break

    return start_packet_position, start_message_position


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with profile(opt.submission) as results:
        data = open(inputpath).read()
        result1, result2 = solution(data)
        results["part1"] = result1
        results["part2"] = result2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
