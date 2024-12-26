import argparse
from functools import reduce
import os


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def read(args):
    """ Parse input """
    if args.submission:
        filepath = "input.txt"
    else:
        filepath = "example_input.txt"

    return open(filepath, "r", encoding="utf-8")


def printr(results):
    """ Print results """
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")

    print("--------------------")

if __name__ == "__main__":
    opt = get_args()
    data = read(opt).read().strip().split(',')

    def char(i, c): 
        return (i+ord(c)) * 17 % 256
    
    def hash(s): 
        return reduce(char, s, 0)
    
    part_1 = sum(map(hash, data))

    boxes = [dict() for _ in range(256)]

    for step in data:
        match step.strip('-').split('='):
            case [l, f]: boxes[hash(l)][l] = int(f) # Assignment
            case [l]:    boxes[hash(l)].pop(l, 0) # Removal

    part_2 = sum(i*j*f for i,b in enumerate(boxes, 1)
                    for j,f in enumerate(b.values(), 1))
    
    printr([part_1, part_2])

