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


def solution(inp):
    # part 1
    inp = inp.readlines()
    for i in range(len(inp)):
        inp[i] = [c for c in inp[i][:-1]]
    #print(inp)
    visible = 0
    for i,row in enumerate(inp):
        if i == 0 or i == len(inp)-1:
            visible += len(row)-2
        for j, val in enumerate(row):
            if j == 0 or j == len(row) - 1:
                visible += 1
            elif 0 < i < len(inp)-1:
                if not False in [val > z for z in inp[i][:j]] or not False in [val > z for z in inp[i][j+1:]] or not False in [val > z for z in [inp[z][j] for z in range(i)]] or not False in [val > z for z in [inp[z][j] for z in range(i+1, len(inp[0]))]]:
                    visible += 1

    part1 = visible
    # part 2
    best_score = 0
    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    for i,row in enumerate(inp):
        for j, val in enumerate(row):
            score = 1
            for (direction_row,direction_col) in directions:                        
                distance = 1
                cur_row = i+direction_row
                cur_col = j+direction_col
                while True:
                    if not (0<=cur_row<len(row) and 0<=cur_col<len(inp)):
                        distance -= 1
                        break

                    if inp[cur_row][cur_col]>=inp[i][j]:
                        break
                    distance += 1
                    cur_row += direction_row
                    cur_col += direction_col
                score *= distance
            best_score = score if score > best_score else best_score

    part2 = best_score
    return part1, part2


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with profile(opt.submission) as results:
        data = open(inputpath)
        result1, result2 = solution(data)
        results["part1"] = result1
        results["part2"] = result2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
