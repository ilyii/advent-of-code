import argparse
import os
from collections import defaultdict, deque
from itertools import product
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def count_arrangements(spring_row, groups):
    question_indices = [i for i, char in enumerate(spring_row) if char == '?']
    possible_arrangements = 0

    for replacements in product('.#', repeat=len(question_indices)):
        row = list(spring_row)
        for idx, char in zip(question_indices, replacements):
            row[idx] = char
        row = ''.join(row)

        block_sizes = [len(block) for block in row.split('.') if block]
        if block_sizes == groups:
            possible_arrangements += 1

    return possible_arrangements

def submission(data):
    return sum(count_arrangements(spring_row, groups) for spring_row, groups in data),0

def main():
    inputpath = "example_input.txt"

    opt = get_args()
    if opt.submission:
        inputpath = "input.txt"

    with open(inputpath, "r") as file:
        data = file.read().splitlines()
    
    data = [line.split() for line in data]
    data = [(line[0], list(map(int, line[1].split(",")))) for line in data]
    data = [("?".join(5*sequence), 5*groups) for sequence, groups in data]
    print(data)
    result1, result2  = submission(data)

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()