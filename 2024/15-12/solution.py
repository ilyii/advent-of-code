import argparse
from collections import deque
from itertools import cycle
import os
from numbers import Number
from typing import Any, Set, Tuple

import numpy as np



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def submission(data: Any) -> Tuple[int, int]:
    """ Logic """
    grid, movements = data
    W,H = grid.shape
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    walls = np.transpose(np.where(grid == "#"))
    boxes = np.transpose(np.where(grid == "O"))
    walls_set = set((int(row[0]), int(row[1])) for row in walls)
    boxes_set = set((int(row[0]), int(row[1])) for row in boxes)

    def push(pos, direction, boxes, walls):
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos in walls:
            return False, boxes
        
        if next_pos in boxes:
            success, new_boxes = push(next_pos, direction, boxes, walls)

            if success:
                return push(pos, direction, new_boxes, walls)
            else:
                return False, boxes
        
        new_boxes = boxes.copy()
        new_boxes.remove(pos)
        new_boxes.add(next_pos)
        return True, new_boxes


    def move(pos, direction, boxes, walls):
        """Moves the robot and recursively pushes boxes."""
        global grid
        delta = directions[direction]
        next_pos = (pos[0] + delta[0], pos[1] + delta[1])

        if next_pos in walls:
            return pos, boxes

        elif next_pos in boxes:
            success, new_boxes = push(next_pos, delta, boxes, walls)

            if success:
                return next_pos, new_boxes
            else:
                return pos, boxes
        return next_pos, boxes
            
            

    
    robot = np.ravel(np.transpose(np.where(grid == "@")))

    for idx,move_dir in enumerate(movements):
        robot, boxes_set = move(robot, move_dir, boxes_set, walls_set)

    part1 = sum([100*i[0] + i[1] for i in boxes_set])


    # ---- PART 2 ---- #
    # '#': '##'
    # 'O': '[]'
    # '.': '..'
    # '@': '@.'

    
    walls_2 = set((row, col * 2) for row, col in walls_set)
    walls_2.update((row, col * 2 + 1) for row, col in walls_set)  
    boxes_2 = set(((row, col * 2), (row, col * 2 + 1)) for row, col in boxes_set)
    robot_2 = (robot[0], robot[1] * 2) 
    

    def visualize(robot: Tuple[int, int], walls: Set[Tuple[int, int]], 
                    boxes: Set[Tuple[Tuple[int, int], Tuple[int, int]]], char: str):
        """Prints the current state of the grid for visualization."""
        b = cycle('[]')  # Alternating box characters
        plain_boxes = {tile for box in boxes for tile in box}
        print(f"Move: {char}")
        for r in range(W*2):
            for c in range(H*2):
                if (r, c) == robot:
                    print("@", end="")
                elif (r, c) in walls:
                    print("#", end="")
                elif (r, c) in plain_boxes:
                    print(next(b), end="")
                else:
                    print(".", end="")
            print()
        print("=" * H*2)
        print()

    def push_2(box, direction, walls, boxes):
        d = directions[direction]
        next_tile_left = (box[0][0] + d[0], box[0][1] + d[1])
        next_tile_right = (box[1][0] + d[0], box[1][1] + d[1])
        next_box = (next_tile_left, next_tile_right)
        
        if next_tile_left in walls or next_tile_right in walls or next_box in boxes:
            return False, boxes  # Blocked

        new_boxes = boxes.copy()
        new_boxes.remove(box)
        new_boxes.add(next_box)
        return True, new_boxes

    def move_2(robot, direction, walls, boxes):
        d = directions[direction]
        next_tile = (robot[0] + d[0], robot[1] + d[1])

        if next_tile in walls:
            return robot, boxes  

        for box in boxes:
            if next_tile in box:
                success, new_boxes = push_2(box, direction, walls, boxes)
                if not success:
                    return robot, boxes
                return next_tile, new_boxes

        return next_tile, boxes

    visualize(robot_2, walls_2, boxes_2, "INIT")
    for i, char in enumerate(movements):
        robot_2, boxes_2 = move_2(robot_2, char, walls_2, boxes_2)
        visualize(robot_2, walls_2, boxes_2, char)
        
    part2 = sum(100 * i[0][0] + i[0][1] for i in boxes_2)
    
    return part1, part2
    


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read()
    
    grid, movements = data.split("\n\n")
    grid = np.array([list(row) for row in grid.split("\n")])
    movements = list("".join(char for char in movements if char in "<>^v"))
    
    data = [grid, movements]
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