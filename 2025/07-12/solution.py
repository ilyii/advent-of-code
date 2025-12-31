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

def solve(grid_str):
    lines = [line.strip('\n') for line in grid_str.splitlines() if line.strip()]
    height, width = len(lines), len(lines[0])
    
    has_beam = [[False] * width for _ in range(height)] # Track where beams are present
    path_count = [[0] * width for _ in range(height)] # Track number of timelines reaching each cell
    
    # Find the source S
    start_x = lines[0].find('S')
    has_beam[0][start_x] = True
    path_count[0][start_x] = 1
    
    activated_splitters = set()
    total_timelines = 0

    for y in range(height):
        for x in range(width):
            if not has_beam[y][x]:
                continue
                
            # If we are at the bottom row, these timelines are finished
            if y == height - 1:
                total_timelines += path_count[y][x]
                continue
            
            char_below = lines[y+1][x]
            
            if char_below == '^':
                # Part 1
                activated_splitters.add((x, y+1))
                
                # Part 2
                for dx in [-1, 1]:
                    nx = x + dx
                    if 0 <= nx < width:
                        has_beam[y+1][nx] = True
                        path_count[y+1][nx] += path_count[y][x]
            else:
                # Beam continues straight down
                has_beam[y+1][x] = True
                path_count[y+1][x] += path_count[y][x]
                
    return len(activated_splitters), total_timelines

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)  # or read(opt), read_grid(opt)

    with profile(opt.submission) as results:
        result1, result2 = solve(data)


        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
