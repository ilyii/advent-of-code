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


def read_ints(args):
    """Parse input - returns list of integers"""
    return [int(x) for x in read_lines(args)]


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

def get_accessible_rolls(grid):
    """
    An accessible roll is defined as a `@` cell that has 'fewer than 4' adjacent `@` cells in the eight adjacent positions.
    """
    accessible_rolls = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                adjacent_count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        adjacent_count += 1
                if adjacent_count < 4:
                    accessible_rolls.append((r, c))

    return accessible_rolls

if __name__ == "__main__":
    opt = get_args()
    data = read_grid(opt)

    with profile(opt.submission) as results:
        result1 = 0
        result2 = 0

        # Solve both parts here
        accessible_rolls = get_accessible_rolls(data)
        result1 = len(accessible_rolls)
        result2 += len(accessible_rolls)
        while len(accessible_rolls) > 0:
            for ar in accessible_rolls:
                data[ar[0]][ar[1]] = '.'
            accessible_rolls = get_accessible_rolls(data)
            result2 += len(accessible_rolls)

        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
