import argparse
import os
import sys
import bisect

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
    if not os.path.exists(filepath):
        # Fallback for testing if file doesn't exist
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def solve(input_data):
    """ 
    Idea: Iterate through all the possible patterns, which are formed by repeating a base number.
    For each base number, generate numbers by repeating it k times (k >= 2).
    """
    if not input_data:
        return 0, 0

    ranges = []
    max_val = 0
    # Clean up whitespace and handle potential trailing commas
    raw_ranges = input_data.replace('\n', '').strip().split(',')
    for r in raw_ranges:
        if '-' in r:
            low, high = map(int, r.split('-'))
            ranges.append((low, high))
            max_val = max(max_val, high)

    # Set to avoid duplicates
    p1_pool = set()
    p2_pool = set()
    
    max_len = len(str(max_val))

    # Max length of base equals max_len // 2
    for length in range(1, (max_len // 2) + 1):
        start = 10**(length - 1)
        end = 10**length
        
        for n in range(start, end):
            base_str = str(n)
            
            k = 2
            while True:
                candidate_str = base_str * k
                if len(candidate_str) > max_len:
                    break
                
                candidate_int = int(candidate_str)
                if candidate_int > max_val:
                    break
                
                # Part 1
                if k == 2:
                    p1_pool.add(candidate_int)
                
                # Part 2
                p2_pool.add(candidate_int)
                k += 1

    sorted_p1 = sorted(list(p1_pool))
    sorted_p2 = sorted(list(p2_pool))

    part1_total = 0
    part2_total = 0
    
    for low, high in ranges:
        # Sum for Part 1
        idx1 = bisect.bisect_left(sorted_p1, low)
        while idx1 < len(sorted_p1) and sorted_p1[idx1] <= high:
            part1_total += sorted_p1[idx1]
            idx1 += 1
            
        # Sum for Part 2
        idx2 = bisect.bisect_left(sorted_p2, low)
        while idx2 < len(sorted_p2) and sorted_p2[idx2] <= high:
            part2_total += sorted_p2[idx2]
            idx2 += 1
            
    return part1_total, part2_total

def printr(*results):
    """ Print results """
    folder = os.path.dirname(__file__).split(os.sep)[-1] or "Advent of Code"
    print(f"-----{folder}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)
    
    with profile(opt.submission) as results:
        res1, res2 = solve(data)
        results["part1"] = res1
        results["part2"] = res2
    
    printr(res1, res2)