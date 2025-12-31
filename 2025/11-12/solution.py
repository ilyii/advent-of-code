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


def printr(*results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

# ----------------------------------- #
# ----------- Custom Code ----------- #
# ----------------------------------- #

def count_paths(mapper, start, required=frozenset()):
    """Count paths from start to 'out', optionally requiring certain nodes to be visited."""
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dfs(node, visited):
        visited = visited | ({node} & required)  # Track only required nodes
        
        if node == 'out':
            return 1 if visited == required else 0
        if node not in mapper:
            return 0
        
        return sum(dfs(dst, visited) for dst in mapper[node])
    
    return dfs(start, frozenset())

def solve(data):
    mapper = {}
    for line in data.splitlines():
        src, dst = line.split(": ")
        mapper[src] = dst.split(" ")
    
    part1 = count_paths(mapper, "you")
    part2 = count_paths(mapper, "svr", frozenset({"dac", "fft"}))
    
    return part1, part2

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)

    with profile(opt.submission) as results:
        result1, result2 = solve(data)

        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
