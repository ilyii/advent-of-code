import argparse
import os
import sys
import time
from itertools import count

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

DIRECTIONS = {(-1, 0): '|F7', # Up
              (1, 0): '|LJ', # Down
              (0, -1): '-FL', # Left
              (0, 1): '-J7', # Right
			  } 


def add(ra, ca, rb, cb):
	return ra + rb, ca + cb


def find_start(grid):
	return next((r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 'S')


def part1(grid):
	row_start, col_start = find_start(grid)
	matches = list()

	for (dr, dc), pipes in DIRECTIONS.items():
		r, c = row_start + dr, col_start + dc
		if grid[r][c] in pipes:
			matches.append((dr, dc))

	assert len(matches) == 2, 'The start pipe must have exactly two adjacent pipes.'

	U, D, L, R = DIRECTIONS.keys()
	if   matches == [U, D]: start_pipe = '|'
	elif matches == [L, R]: start_pipe = '-'
	elif matches == [U, L]: start_pipe = 'J'
	elif matches == [U, R]: start_pipe = 'L'
	elif matches == [D, L]: start_pipe = '7'
	elif matches == [D, R]: start_pipe = 'F'
	else: raise ValueError('Invalid start pipe')

	r, c = row_start, col_start
	dr, dc = matches[0]
	seen = set([(r, c)])

	i = 0
	while True:
		i += 1
		r, c = r + dr, c + dc
		pipe = grid[r][c]
		seen.add((r, c))

		if pipe in 'L7':
			dr, dc = dc, dr
		elif pipe in 'FJ':
			dr, dc = -dc, -dr
		elif pipe == 'S':
			break
			
	
	grid[row_start][col_start] = start_pipe
	return seen, i


def part2(grid, main_loop):
	area = 0

	for r, row in enumerate(grid):
		inside = False
		for c, cell in enumerate(row):
			"""
			1. We are inside the main loop if we are not in the main loop and the cell is a pipe.
			2. We are outside the main loop if we are in the main loop and the cell is not a pipe.
			"""
			if (r, c) not in main_loop:
				area += inside
			else:				
				inside = inside ^ (cell in '|F7')

	return area



def main(data):
	grid = [list(line.rstrip()) for line in data.splitlines()]
	main_loop, loop_len = part1(grid)
	max_pipe_distance = loop_len // 2
	print('Part 1:', max_pipe_distance)

	area = part2(grid, main_loop)
	print('Part 2:', area)


if __name__ == "__main__":
    opt = get_args()
    inputpath = "input.txt" if opt.submission else "example_input.txt"
    
    with open(inputpath) as f:
        data = f.read().strip()

    with profile(opt.submission) as results:
        grid = [list(line.rstrip()) for line in data.splitlines()]
        main_loop, loop_len = part1(grid)
        max_pipe_distance = loop_len // 2
        area = part2(grid, main_loop)
        results["part1"] = max_pipe_distance
        results["part2"] = area

    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {max_pipe_distance}")
    print(f"Part 2: {area}")

