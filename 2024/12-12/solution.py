import os
import sys
import argparse
import numpy as np
from scipy.ndimage import label, convolve

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def calculate_metrics(data):
    chars = np.unique(data)
    total_perimeter, total_edges = 0, 0
    
    for char in chars:
        labeled_grid, num_regions = label(data == char)
        
        for region_id in range(1, num_regions + 1):
            region = (labeled_grid == region_id).astype(int)
            area = np.count_nonzero(region)
            padded_region = np.pad(region, 1)
            
            kernel = np.array([[1, -1], [0, 0]])
            border_count = lambda mask: np.count_nonzero(convolve(mask, kernel))
            perimeter = sum(border_count(np.rot90(padded_region, k=i)) for i in range(4))
            
            edges = sum(label(convolve(np.rot90(padded_region, k=i), kernel) == 1)[1] for i in range(4))

            total_perimeter += perimeter*area //2
            total_edges += edges*area

    return total_perimeter, total_edges

def main():
    opt = get_args()
    input_file = "input.txt" if opt.submission else "example_input.txt"
    
    with open(input_file, "r") as file:
        data = np.array([list(line) for line in file.read().splitlines()])
    print(data)

    with profile(opt.submission) as results:
        result1, result2 = calculate_metrics(data)
        results["part1"] = result1
        results["part2"] = result2

    print(f"-----{os.path.basename(os.getcwd())}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

if __name__ == "__main__":
    main()
