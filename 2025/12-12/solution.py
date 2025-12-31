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


def printr(*results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

# ----------------------------------- #
# ----------- Custom Code ----------- #
# ----------------------------------- #

def parse_input(data):
    """Parse shapes and regions from input."""
    parts = data.split('\n\n')
    shapes = {}
    regions = []
    
    for part in parts:
        lines = part.strip().split('\n')
        if lines[0].endswith(':') and lines[0][:-1].isdigit():
            # Shape definition
            idx = int(lines[0][:-1])
            coords = frozenset(
                (r, c)
                for r, line in enumerate(lines[1:])
                for c, ch in enumerate(line)
                if ch == '#'
            )
            shapes[idx] = coords
        else:
            # Region definitions
            for line in lines:
                if 'x' in line and ': ' in line:
                    dim_part, counts_part = line.split(': ')
                    w, h = map(int, dim_part.split('x'))
                    counts = list(map(int, counts_part.split()))
                    regions.append((w, h, counts))
    
    return shapes, regions


def normalize(coords):
    """Normalize coordinates to start at (0,0)."""
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)


def get_all_orientations(coords):
    """Get all unique orientations (rotations + flips) of a piece."""
    orientations = set()
    current = coords
    
    for _ in range(4):
        orientations.add(normalize(current))
        orientations.add(normalize(frozenset((r, -c) for r, c in current)))  # flip
        current = frozenset((c, -r) for r, c in current)  # rotate 90° CW
    
    return list(orientations)


def solve_region(width, height, pieces, shape_orientations, shape_sizes):
    """
    Backtracking solver using "fill first empty cell" heuristic.
    For slack cases, we mark cells as "blocked" to skip them.
    """
    if not pieces:
        return True
    
    # Quick area check
    total_piece_area = sum(shape_sizes[idx] for idx in pieces)
    grid_area = width * height
    if total_piece_area > grid_area:
        return False
    
    slack = grid_area - total_piece_area
    
    # Grid: 0 = empty, 1 = filled by piece, 2 = blocked (slack)
    grid = [[0] * width for _ in range(height)]
    
    def can_place(orientation, pos_r, pos_c):
        for r, c in orientation:
            nr, nc = pos_r + r, pos_c + c
            if nr < 0 or nr >= height or nc < 0 or nc >= width:
                return False
            if grid[nr][nc] != 0:
                return False
        return True
    
    def place(orientation, pos_r, pos_c):
        for r, c in orientation:
            grid[pos_r + r][pos_c + c] = 1
    
    def unplace(orientation, pos_r, pos_c):
        for r, c in orientation:
            grid[pos_r + r][pos_c + c] = 0
    
    def find_first_empty():
        for r in range(height):
            for c in range(width):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    
    def backtrack(piece_idx, remaining_slack):
        if piece_idx == len(pieces):
            return True
        
        # Find first empty cell
        pos = find_first_empty()
        if pos is None:
            return piece_idx == len(pieces)
        
        target_r, target_c = pos
        shape_idx = pieces[piece_idx]
        
        # Try placing a piece that covers this cell
        for orientation in shape_orientations[shape_idx]:
            for cell_r, cell_c in orientation:
                pos_r = target_r - cell_r
                pos_c = target_c - cell_c
                
                if can_place(orientation, pos_r, pos_c):
                    place(orientation, pos_r, pos_c)
                    if backtrack(piece_idx + 1, remaining_slack):
                        return True
                    unplace(orientation, pos_r, pos_c)
        
        # If we have slack, try leaving this cell empty (block it)
        if remaining_slack > 0:
            grid[target_r][target_c] = 2  # block
            if backtrack(piece_idx, remaining_slack - 1):
                return True
            grid[target_r][target_c] = 0  # unblock
        
        return False
    
    return backtrack(0, slack)


def solve(data):
    shapes, regions = parse_input(data)
    
    # Precompute orientations and sizes
    shape_orientations = {idx: get_all_orientations(coords) for idx, coords in shapes.items()}
    shape_sizes = {idx: len(coords) for idx, coords in shapes.items()}
    
    # Count solvable regions
    solvable = 0
    
    for w, h, counts in regions:
        # Build piece list: sort by shape for duplicate elimination
        pieces = []
        for shape_idx, count in enumerate(counts):
            pieces.extend([shape_idx] * count)
        
        # Sort pieces (group same shapes together, larger shapes first for better pruning)
        pieces.sort(key=lambda x: (-shape_sizes[x], x))
        
        if solve_region(w, h, pieces, shape_orientations, shape_sizes):
            solvable += 1
    
    return solvable, None

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)

    with profile(opt.submission) as results:
        result1, result2 = solve(data)

        # Solve both parts here

        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
