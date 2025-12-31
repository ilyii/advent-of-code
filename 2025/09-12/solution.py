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

from bisect import bisect_left, bisect_right

def solve_both(data):
    """
    Solve Part 1 and Part 2 together - highly optimized.
    """
    # Parse coordinates - optimized parsing
    coords = []
    for line in data:
        if line:
            i = line.index(',')
            coords.append((int(line[:i]), int(line[i+1:])))
    
    n = len(coords)
    if n < 2:
        return 0, 0
    
    # Build segments using plain dicts (faster than defaultdict)
    h_by_y = {}
    v_by_x = {}
    v_all = []
    
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        
        if y1 == y2:
            if x1 > x2: x1, x2 = x2, x1
            if y1 in h_by_y:
                h_by_y[y1].append((x1, x2))
            else:
                h_by_y[y1] = [(x1, x2)]
        else:
            if y1 > y2: y1, y2 = y2, y1
            v_all.append((x1, y1, y2))
            if x1 in v_by_x:
                v_by_x[x1].append((y1, y2))
            else:
                v_by_x[x1] = [(y1, y2)]
    
    # Pre-sort for binary search
    v_all.sort()
    v_xs = [s[0] for s in v_all]
    h_ys = sorted(h_by_y)
    v_xs_unique = sorted(v_by_x)
    
    # Cache with pre-populated red tiles
    cache = {c: True for c in coords}
    
    # Localize for inner loop speed
    bl, br = bisect_left, bisect_right
    
    def valid(px, py):
        k = (px, py)
        r = cache.get(k)
        if r is not None:
            return r
        
        # Boundary check
        segs = h_by_y.get(py)
        if segs:
            for x1, x2 in segs:
                if x1 <= px <= x2:
                    cache[k] = True
                    return True
        
        segs = v_by_x.get(px)
        if segs:
            for y1, y2 in segs:
                if y1 <= py <= y2:
                    cache[k] = True
                    return True
        
        # Ray cast
        c = 0
        for i in range(bl(v_xs, px)):
            _, y1, y2 = v_all[i]
            if y1 < py <= y2:
                c += 1
        
        r = c & 1
        cache[k] = r
        return r
    
    def rect_ok(x1, y1, x2, y2):
        # Corners
        if not valid(x1, y1) or not valid(x1, y2) or not valid(x2, y1) or not valid(x2, y2):
            return False
        
        # H-segments crossing interior
        for i in range(br(h_ys, y1), bl(h_ys, y2)):
            y = h_ys[i]
            for sx1, sx2 in h_by_y[y]:
                if sx1 < x2 and sx2 > x1:
                    if (sx1 <= x1 and sx2 >= x2) or (x1 < sx1 < x2) or (x1 < sx2 < x2):
                        return False
        
        # V-segments crossing interior
        for i in range(br(v_xs_unique, x1), bl(v_xs_unique, x2)):
            x = v_xs_unique[i]
            for sy1, sy2 in v_by_x[x]:
                if sy1 < y2 and sy2 > y1:
                    if (sy1 <= y1 and sy2 >= y2) or (y1 < sy1 < y2) or (y1 < sy2 < y2):
                        return False
        
        return True
    
    # Build pairs - inline min/max with conditionals
    pairs = []
    append = pairs.append
    for i in range(n):
        ax, ay = coords[i]
        for j in range(i + 1, n):
            bx, by = coords[j]
            x1, x2 = (ax, bx) if ax < bx else (bx, ax)
            y1, y2 = (ay, by) if ay < by else (by, ay)
            append(((x2 - x1 + 1) * (y2 - y1 + 1), x1, y1, x2, y2))
    
    pairs.sort(reverse=True)
    
    p1 = pairs[0][0]
    p2 = 0
    
    for a, x1, y1, x2, y2 in pairs:
        if a <= p2:
            break
        if rect_ok(x1, y1, x2, y2):
            p2 = a
            break
    
    return p1, p2


if __name__ == "__main__":
    opt = get_args()
    data = read_lines(opt)

    with profile(opt.submission) as results:
        result1, result2 = solve_both(data)

        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
