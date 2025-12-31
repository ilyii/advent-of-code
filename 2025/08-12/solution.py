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


def read(args):
    """Parse input - returns file content as string"""
    filepath = "input.txt" if args.submission else "example_input.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def read_lines(args):
    """Parse input - returns list of lines"""
    return read(args).split("\n")


def read_grid(args):
    """Parse input - returns 2D grid of characters"""
    return [list(line) for line in read_lines(args)]


def print_grid(grid):
    """Print 2D grid"""
    for row in grid:
        print("".join(row))

def printr(*results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

# ----------------------------------- #
# ----------- Custom Code ----------- #
# ----------------------------------- #


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_sets = n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.num_sets -= 1
            return True 
        return False 


def solve(data):
    coords = []
    for line in data:
        if not line.strip(): continue
        coords.append(list(map(int, line.split(","))))
    
    num_nodes = len(coords)
    
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dz = coords[i][2] - coords[j][2]
            dist_sq = dx*dx + dy*dy + dz*dz
            edges.append((dist_sq, i, j))
    
    edges.sort()

    # Part 1
    dsu = DSU(num_nodes)
    for k in range(min(1000, len(edges))):
        _, u, v = edges[k]
        dsu.union(u, v)
        
    part1 = 1
    for s in sorted([dsu.size[i] for i in range(num_nodes) if dsu.parent[i] == i], reverse=True)[:3]:
        part1 *= s

    # Part 2
    dsu = DSU(num_nodes)
    part2 = 0
    
    # Iterate through ALL sorted edges
    for _, u, v in edges:
        if dsu.union(u, v):
            if dsu.num_sets == 1:
                part2 = coords[u][0] * coords[v][0]
                break
                
    return part1, part2


if __name__ == "__main__":
    opt = get_args()
    data = read_lines(opt)  # or read(opt), read_grid(opt)

    with profile(opt.submission) as results:
        result1, result2 = solve(data)


        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
