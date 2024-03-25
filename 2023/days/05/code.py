import time
import re


def apply(v, tuples):
    for d,s,r in tuples:
        if s<=v<(s+r):            
            return v+d-s
    return v

def apply_range(R: list[tuple[int,int]], tuples: list[tuple[int,int,int]]) -> list[tuple[int,int]]:
    """
    Shoutout to jonathanpaulson for this solution - otherwise my compiler would still be running.
    """
    A = []
    for d,s,r in tuples:
        NR = []
        for start,end in R:
            if start < min(end,s): # range is before the tuple
                NR.append((start, min(end,s)))
            if max(s+r, start) < end: # range is after the tuple
                NR.append((max(s+r, start), end))
            if max(start, s) < min(s+r, end): # range is inside the tuple
                A.append((max(start, s)-s+d, min(s+r, end)-s+d))

        R = NR
    return A+R

def part1(data):
    data = data.split("\n\n")
    N = [int(x) for x in re.findall(r'\d+', data[0])]
    for i, _ in enumerate(N):
        
        for map in data[1:]:
            map = map.split("\n")[1:]
            tuples = [[int(x) for x in line.split()]for line in map]
            N[i] = apply(N[i], tuples)

    return min(N)


def part2(data):
    data = data.split("\n\n")
    seeds = [int(x) for x in re.findall(r'\d+', data[0])]
    pairs = list(zip(seeds[::2], seeds[1::2])) # [1,2,3,4] -> [(1,2),(3,4)]
    N = []
    for i, (s, r) in enumerate(pairs):
        R = [(s, s+r)]
        for map in data[1:]:
            map = map.split("\n")[1:]
            tuples = [[int(x) for x in line.split()]for line in map] # ["1 2 3", "4 5 6"] -> [[1,2,3],[4,5,6]]
            R = apply_range(R, tuples)
        N.append(min(R)[0])
    return min(N)



if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1 = part1(data)
    s2 = time.time()
    print(f"\nAnswer 1: {answer_1}")
    s3 = time.time()
    answer_2 = part2(data)
    s4 = time.time()
    print(f"Answer 2: {answer_2}\n")    
    
    print(f'Times: {(s2-s1)*1000:.4f}ms, {(s4-s3)*1000:.4f}ms')