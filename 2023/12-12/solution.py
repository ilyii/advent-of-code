import argparse
from collections import deque
import os
from functools import cache



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()



@cache
def combinate(lava, springs, result=0):
    if not springs:
        return '#' not in lava
    current, springs = springs[0], springs[1:]
    for i in range(len(lava) - sum(springs) - len(springs) - current + 1):
        if "#" in lava[:i]:
            break
        if (nxt := i + current) <= len(lava) and '.' not in lava[i : nxt] and lava[nxt : nxt + 1] != "#":
            result += combinate(lava[nxt + 1:], springs)
    return result



def submission(data):
    data = [line.split() for line in data]
    
    part_1 = 0
    for idx, (lava, springs) in enumerate(data):
        springs = tuple(map(int, springs.split(",")))
        part_1 += combinate(lava, springs)

    
    part_2 = 0
    for idx, (lava, springs) in enumerate(data):
        lava = "?".join([lava] * 5)
        springs = tuple(map(int, springs.split(","))) * 5
        part_2 += combinate(lava, springs)

    return part_1, part_2


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read().splitlines()
    
    # ---- SUBMISSION ---- #
    result1, result2 = submission(data)

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

    if opt.submission:
        import timeit
        res = timeit.timeit(lambda: submission(data), number=10)
        print(f"Time: {res/10:.7f}s")