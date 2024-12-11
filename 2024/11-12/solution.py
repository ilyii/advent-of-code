import argparse
import os
from collections import Counter, defaultdict, deque

import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def submission(stones):
    def process(counter, iterations):
        current_state = Counter(counter)

        for _ in range(iterations):
            new_state = Counter()
            for stone, count in current_state.items():
                if stone == 0: # 0
                    new_state[1] += count  
                else:
                    stone_str = str(stone)
                    length = len(stone_str)
                    if length % 2 == 0:  # Even
                        mid = length // 2
                        left = int(stone_str[:mid])
                        right = int(stone_str[mid:])
                        new_state[left] += count
                        new_state[right] += count
                    else:  # Odd
                        new_state[stone * 2024] += count
            current_state = new_state

        return sum(current_state.values())

    counter = Counter(stones)
    return process(counter, 25), process(counter, 75)


def main():
    inputpath = "example_input.txt"

    opt = get_args()
    if opt.submission:
        inputpath = "input.txt"

    with open(inputpath, "r") as file:
        data = file.read().splitlines()
    data = np.array(list(map(int, data[0].split())))
    
    
    result1, result2 = submission(data)

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()