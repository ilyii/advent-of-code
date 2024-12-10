import re
import math
from collections import defaultdict


def calculate(data):
    symbols = {
        (i, j)
        for i, l in enumerate(data)
        for j, x in enumerate(l)
        if not x.isalnum() and not x == "." 
    }
    numbers = re.compile(r"(\d+)")

    symbol_numbers = defaultdict(list)
    for i, line in enumerate(data):
        for match in numbers.finditer(line):
            n = int(match.group(0))
            box = {
                (i + di, j + dj)
                for di in range(-1, 2)
                for dj in range(-1, 2)
                for j in range(match.start(), match.end())
            }
            for s in symbols & box:
                symbol_numbers[s].append(n)
    return symbol_numbers


if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    answer_1 = sum(sum(v) for v in calculate(data.splitlines()).values())
    print(f"Answer 1: {answer_1}")

    answer_2 = sum(math.prod(v) for v in calculate(data.splitlines()).values() if len(v) == 2)
    print(f"Answer 2: {answer_2}")

