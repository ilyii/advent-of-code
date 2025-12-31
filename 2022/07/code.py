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


def solution(file):
    folder_sizes = {}
    folder_path = []

    for line in file.readlines():
        cmd = line.split()
        if cmd[0] == "$":
            if cmd[1] == "cd":
                if cmd[2] == "..":
                    folder_path = folder_path[:-1]
                elif cmd[2] == "/":
                    folder_path = ["/"]
                else:
                    folder_path.append(cmd[2])
        else:
            if cmd[0] != "dir":
                current_path = ""
                for folder in folder_path:
                    if current_path != "/" and folder != "/":
                        current_path += "/"
                    current_path += folder
                    folder_sizes[current_path] = folder_sizes.get(current_path, 0) + int(cmd[0])

    # Part 1
    part1 = sum(value for name, value in folder_sizes.items() if value < 100000)

    # Part 2
    needed_space = 30000000 - (70000000 - folder_sizes.get("/"))
    part2 = min(value for name, value in folder_sizes.items() if value >= needed_space)
    
    return part1, part2


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with profile(opt.submission) as results:
        with open(inputpath) as file:
            result1, result2 = solution(file)
        results["part1"] = result1
        results["part2"] = result2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

