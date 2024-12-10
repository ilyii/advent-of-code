import time
import re
import math

def part1(data):
    times, distances = map(lambda x: list(map(int, re.findall(r'\d+', x))), data.splitlines())
    prod = []
    for t, d in zip(times, distances):
        prod.append(sum([((t-x)*x) > d for x in range(t+1)]))
    return math.prod(prod)


def part2(data):
    t,d = [int("".join(re.findall(r'\d+', l))) for l in data.splitlines()]
    lower_bound = next(x for x in range(t + 1) if (t - x) * x > d)
    upper_bound = next(x for x in reversed(range(t + 1)) if (t - x) * x > d)

    return upper_bound - lower_bound + 1

    



if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1 = part1(data)
    s2 = time.time()
    print(f"Answer 1: {answer_1}")

    s3 = time.time()
    answer_2 = part2(data)
    s4 = time.time()
    print(f"Answer 2: {answer_2}")    
    
    print(f'Times: {(s2-s1)*1000:.4f}ms, {(s4-s3)*1000:.4f}ms')
