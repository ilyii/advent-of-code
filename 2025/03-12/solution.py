import argparse
import os
import sys

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def read(args):
    """ Parse input """
    filepath = "input.txt" if args.submission else "example_input.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()


def printr(*results):
    """ Print results """
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

def _algorithm(bank, k):
    """
    Implements the stack-based approach to find the maximum number
    Args:
    - bank: str, the input string representing the bank
    - k: int, length of the max number to find
    Returns:
    - int, the maximum number found
    """
    stack = list()
    n = len(bank.strip())
    for i, digit in enumerate([int(d) for d in bank.strip()]):
        digits_left = n - i - 1 # digits remaining after current

        # 1. Stack not empty
        # 2. Top of stack < current digit
        # 3. Enough digits left to fill k
        while stack and stack[-1] < digit and digits_left + len(stack) >= k:
            stack.pop()

        if len(stack) < k:
            stack.append(digit)

    # Assumption: Now, the stack has k digits and is the largest possible number
    return int(''.join(map(str, stack)))
        

def solve(data):
    """
    Idea: Keep the candidate number as stack to represent the right order. 
    """
    part_1 = 0
    part_2 = 0
    for line in data:
        part_1 += _algorithm(line, 2)
        part_2 += _algorithm(line, 12)

    return part_1, part_2
        



if __name__ == "__main__":
    opt = get_args()
    data = read(opt)

    with profile(opt.submission) as results:
        res1, res2 = solve(data)
        results["part1"] = res1
        results["part2"] = res2

    printr(res1, res2)
