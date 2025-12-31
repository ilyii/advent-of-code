import argparse
import os
import sys
import time
from collections import defaultdict
import re
import math

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def parse(data):
    data = data.splitlines()
    instructions = data[0].strip()
    network = defaultdict(list)
    for line in data[2:]:
        line = line.split(" = ")
        network[line[0]] = re.findall(r"\w+", line[1])

    return instructions, network


def navigate(instructions, network, p2_flag=False):

    s = [k for k in network.keys() if k.endswith("A")] if p2_flag else ["AAA"]
    criterion = "Z" if p2_flag else "ZZZ"

    res = [] 
    for current in s:
        steps = 0
        while True:
            ins = instructions[steps % len(instructions)]
            if ins == "L":
                current = network[current][0]
            elif ins == "R":
                current = network[current][1]
            
            steps += 1
            if current.endswith(criterion):
                res.append(steps)
                break

        
    if p2_flag:        
        common_multiple = res[0]
        for elem in res[1:]:
            common_multiple = common_multiple * elem // math.gcd(common_multiple, elem)
        return common_multiple
    else:
        return res[0]



    
def manage(data, p2_flag=False):
    instructions, network = parse(data)
    
    result = navigate(instructions, network, p2_flag)
    return result


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        answer_1 = manage(data)
        answer_2 = manage(data, p2_flag=True)
        results["part1"] = answer_1
        results["part2"] = answer_2

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")

    