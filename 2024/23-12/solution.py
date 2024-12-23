import argparse
from collections import defaultdict
from itertools import combinations
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
    data = read(opt)

    nodes, edges = set(), set()
    for line in data:
        a, b = line.strip().split('-')
        nodes.update([a, b])
        edges.update([(a,b), (b,a)])

    # 1. Iterate over all possible triplets of nodes
    # 2. Check if the triplet forms a triangle
    # 3. Check if any element starts with a 't'
    part_1 = sum({(a,b), (b,c), (c,a)} < edges
            and 't' in (a + b + c)[::2]
            for a, b, c in combinations(nodes, 3))


    
    # 1. Create an adjacency list representation of the graph
    # 2. Find all connected components in the graph
    # 3. Find the largest component and sort it
    part_2 = [{n} for n in nodes]
    for p in part_2:
        for n in nodes:
            if all((n, m) in edges for m in p):
                p.add(n)

    part_2 = ",".join(sorted(max(part_2, key=len)))

    printr([part_1, part_2])



