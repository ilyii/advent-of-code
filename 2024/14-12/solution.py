import argparse
import os
import sys
import re

from collections import Counter
from numbers import Number
import time
from typing import Any, Tuple

import numpy as np
import matplotlib.pyplot as plt

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile




def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


W = 101
H = 103 
NUM_ITER = 100

import numpy as np
from scipy.spatial.distance import pdist

def variance(image):
    coords = np.column_stack(np.where(image == 1))
    pairwise_distances = pdist(coords)
    return np.var(pairwise_distances)



def submission(data:Any) -> Tuple[Number, Number]:
    """ Logic
    Part 1:
    -------
    Just simulate movement for each robot and calcualte the final quadrant of each robot.

    Part 2:
    -------
    Since I don't know what the desired pattern will look like, I conduct the following assumptions:
    1. There will probably be no overlapping robots.
    2. The final pattern has higher density than the average.
    """

    # ---- PART 1 ---- #
    counter = Counter()
    positions, velocities = data

    pos_p1 = [[int(px + vx*NUM_ITER), int(py + vy*NUM_ITER)] for (px, py), (vx, vy) in zip(positions, velocities)]
    pos_p1 = [(px%W, py%H) for px, py in pos_p1]
    for px, py in pos_p1:
        if px == W//2 or py == H//2:
            continue
        if px < W//2 and py < H//2:
            counter[0] += 1
        elif px > W//2 and py < H//2:
            counter[1] += 1
        elif px < W//2 and py > H//2:
            counter[2] += 1
        else:
            counter[3] += 1
    

    # ---- PART 2 ---- #
    min_var_idx = 0
    min_var = np.inf
    initial_img = np.zeros((H, W), dtype=np.uint8)
    idx = 0
    while True:
        idx += 1
        img = np.zeros((H, W), dtype=np.uint8)
        for (px,py), (vx, vy) in zip(positions, velocities):
            
            px += vx*idx
            py += vy*idx
            px %= W
            py %= H
            # if img[py, px] == 1:
            #     break
            img[py, px] = 1
        
        if np.all(img == initial_img):
            print(f"Loop detected at {idx}")

        coords = np.column_stack(np.where(img == 1))
        pairwise_distances = pdist(coords)
        var = np.var(pairwise_distances)
        if var < min_var:
            min_var = var
            min_img = img
            min_var_idx = idx

        if idx == 10000:
            plt.figure()
            plt.title(f"Seconds: {min_var_idx}")
            plt.imshow(min_img)
            plt.savefig("tree.png")
            return int(counter[0]*counter[1]*counter[2]*counter[3]), min_var_idx

    



if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read().splitlines()
        # p=0,4 v=3,-3
    positions = [list(map(int, re.findall(r'(-?\d+)', obj.split()[0])))for obj in data]
    velocities = [list(map(int, re.findall(r'(-?\d+)', obj.split()[1]))) for obj in data]

    data = [positions, velocities]
    
    
    # ---- SUBMISSION ---- #
    with profile(opt.submission) as results:
        result1, result2 = submission(data)
        results["part1"] = result1
        results["part2"] = result2

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")