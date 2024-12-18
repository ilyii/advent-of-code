import argparse
import os
from numbers import Number
import re
from typing import Any, Tuple

import numpy as np
import heapq



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def dijkstra(maze, start, end):
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    H,W = maze.shape
    visited = np.zeros((H,W))
    distance = np.zeros((H,W))

    pq = []
    heapq.heappush(pq, (0, start))

    while pq:
        dist, node = heapq.heappop(pq)
        x,y = node
        if visited[x][y]:
            continue
        visited[x][y] = 1
        distance[x][y] = dist

        if node == end:
            return distance, visited

        for dx,dy in directions:
            new_x, new_y = x+dx, y+dy
            if 0 <= new_x < H and 0 <= new_y < W and maze[new_x][new_y] == ".":
                heapq.heappush(pq, (dist+1, (new_x, new_y)))

    return -1

def dfs(maze, start, end):
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    H,W = maze.shape
    visited = np.zeros((H,W))

    stack = []
    stack.append(start)

    while stack:
        node = stack.pop()
        x,y = node
        if visited[x][y]:
            continue
        visited[x][y] = 1

        if node == end:
            return 1

        for dx,dy in directions:
            new_x, new_y = x+dx, y+dy
            if 0 <= new_x < H and 0 <= new_y < W and maze[new_x][new_y] == ".":
                stack.append((new_x, new_y))

    return 0

def submission(data:Any) -> Tuple[Number, Number]:
    """ Logic """
    H,W = 71,71
    grid = np.array([["." for _ in range(W)] for _ in range(H)])

    NUM_ITER = 1024
    for idx, (x,y) in enumerate(data):
        if idx == NUM_ITER:
            break
        grid[y][x] = "#"
    
    distances, visited = dijkstra(grid, (0,0), (H-1,W-1))

    for idx, (x,y) in enumerate(data[NUM_ITER:]):
        grid[y][x] = "#"
        if not dfs(grid, (0,0), (H-1,W-1)):
            break
    
    return distances[H-1][W-1], f"{x},{y}"


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read()

    data = [list(map(int,re.findall(r"\d+", line))) for line in data.splitlines()]
    
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