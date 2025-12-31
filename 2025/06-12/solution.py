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
def solve_part1(data):
    """Part 1: Numbers are read horizontally (space-separated per row)"""
    *num_lines, op_line = data
    operators = op_line.split()
    
    nums_per_block = [list(map(int, line.split())) for line in num_lines]
    blocks = list(zip(*nums_per_block))  # [(col0_nums), (col1_nums), ...]
    
    total = 0
    for op, nums in zip(operators, blocks):
        if op == '+':
            total += sum(nums)
        elif op == '*':
            prod = 1
            for n in nums:
                prod *= n
            total += prod
    return total


def solve_part2(data):
    """Part 2: Numbers are read vertically (digits stacked per column)"""
    *num_lines, op_line = data
    
    # Pad all lines to same length
    max_len = max(len(line) for line in data)
    num_lines = [line.ljust(max_len) for line in num_lines]
    op_line = op_line.ljust(max_len)
    
    operators = [(i, c) for i, c in enumerate(op_line) if c in '+*']
    
    res = 0
    
    for idx, (pos, op) in enumerate(operators):
        if idx + 1 < len(operators):
            end_pos = operators[idx + 1][0]
        else:
            end_pos = max_len
        
        numbers = []
        for col in range(pos, end_pos):
            digits = ""
            for line in num_lines:
                char = line[col] if col < len(line) else " "
                if char.isdigit():
                    digits += char
            if digits:
                numbers.append(int(digits))
        
        # Apply operator
        if op == '+':
            res += sum(numbers)
        elif op == '*':
            prod = 1
            for n in numbers:
                prod *= n
            res += prod
    
    return res

    

if __name__ == "__main__":
    opt = get_args()
    data = read_lines(opt)  # or read(opt), read_grid(opt)

    with profile(opt.submission) as results:
        result1 = solve_part1(data)
        result2 = solve_part2(data)


        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
