import argparse
import os
import sys
import re
import time
from collections import defaultdict

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def calculate(data):

    
    total = 0
    num_cards = defaultdict(int)
    for i, line in enumerate(data):
        num_cards[i] += 1
        id, wins, cands = re.split(': | \| ', line)
        id = int(re.findall('\d+', id)[0])
        wins, cands = wins.split(), cands.split()
        intersection = len(list(set(cands) & set(wins)))

        # Part 1
        if intersection > 0:          
            total += 2**(intersection-1)
        
        # Part 2
        for card in range(id, id+intersection):
            num_cards[card] += num_cards[i]



    return total, sum(num_cards.values())



if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1, answer_2 = calculate(data.splitlines())
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")  
