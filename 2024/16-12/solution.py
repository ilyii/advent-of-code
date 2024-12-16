import argparse
from collections import defaultdict, deque
import os
from numbers import Number
from typing import Any, Tuple

import numpy as np


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def turn_left(d):
    return (d[1], -d[0])

def turn_right(d):
    return (-d[1], d[0])

# (1,0) -> (0,1) = 1
# (1,0) -> (-1,0) = 2
# (1,0) -> (0,-1) = 1
def calculate_turn_costs(d1, d2):
    if d1 == d2:
        return 0
    if -d1[0] == d2[0] or -d1[1] == d2[1]:
        return 2
    return 1


def hand_on_wall(grid, start, end):
    d = (0,1)
    pos = start
    costs = 0
    while np.any(pos != end):
        costs += 1
        for direction in [d, turn_right(d), turn_left(d), (-d[0], -d[1])]:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if grid[new_pos] in [".", "E", "S"]:
                if d == direction:
                    c = 0
                if -d[0] == direction[0] or -d[1] == direction[1]:
                    c = 2
                c = 1

                costs += c*1000
                d = direction
                break
        pos = (pos[0] + d[0], pos[1] + d[1])
    
    print(f"Found end at {pos}")
    return costs


def bfs(grid, start, end):
    d = (0,1)
    visited = set()
    queue = deque()

    queue.append(start)
    costs = 0
    while queue:
        q = queue.popleft()
        costs += 1
        if np.all(q == end):
            print(f"Found end at {q}")
            return costs
        visited.add(tuple(q))
        for direction in [d, turn_left(d), turn_right(d), (-d[0], -d[1])]:
            new_pos = (q[0] + direction[0], q[1] + direction[1])
            if new_pos not in visited and grid[new_pos] in [".", "E", "S"]:
                queue.append(new_pos)
                if d == direction:
                    c = 0
                if -d[0] == direction[0] or -d[1] == direction[1]:
                    c = 2
                c = 1
                costs += c*1000
    return costs


import heapq
import numpy as np

def dijkstra(grid, start, end):
    d = (0,1)  
    directions = [d, turn_left(d), turn_right(d), (-d[0], -d[1])]

    # Priority queue: (cost, position, direction)
    pq = []
    heapq.heappush(pq, (0, start, d))
    distances = defaultdict(set)

    visited = set()

    while pq:
        cost, current, current_dir = heapq.heappop(pq)
        if tuple(current) in visited:
            continue

        visited.add(tuple(current))

        if np.all(current == end):
            # print(f"Found end at {current}")
            return cost, direction, distances

        for direction in directions:
            new_pos = (current[0] + direction[0], current[1] + direction[1])

            if tuple(new_pos) in visited or grid[new_pos] not in [".", "E", "S"]:
                continue

            if direction == current_dir:
                movement_cost = 0  
            elif direction == (-current_dir[0], -current_dir[1]):
                movement_cost = 2 
            else:
                movement_cost = 1 

            total_cost = cost + 1 + movement_cost * 1000

            distances[new_pos].add(total_cost)
            heapq.heappush(pq, (total_cost, new_pos, direction))

    raise ValueError("Dijkstra failed. No path found.")



def bfs_backwawrds(grid, start, end, distances, min_cost, last_dir):
    start = tuple(start)
    end = tuple(end)
    queue = deque([(min_cost, end, last_dir)])
    res = {start, end}

    while queue:
        s, pos, d = queue.popleft()

        res.add(pos)
        for new_d in [d, turn_left(d), turn_right(d), (-d[0], -d[1])]:
            if grid[(new_pos := (pos[0] + new_d[0], pos[1] + new_d[1]))] == ".":
                for ss in (s - 1, s - 1001):
                    if ss in distances[new_pos]:
                        queue.appendleft((ss, new_pos, new_d))

    return res


def submission(data:Any) -> Tuple[Number, Number]:
    """ Logic """
    
    start = np.ravel(np.transpose(np.where(data == "S")))
    end = np.ravel(np.transpose(np.where(data == "E")))

    costs, last_dir, dists = dijkstra(data, start, end)
    cells = bfs_backwawrds(data, start, end, dists, costs, last_dir)
    
 



    
    return costs, len(cells)


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read()
    
    data = np.array([list(line) for line in data.splitlines()])
    
    
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