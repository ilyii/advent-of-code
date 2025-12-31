from pathlib import Path
import argparse
import sys
import os

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def printr(*results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)


def parse_lines(lines):
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        dirc = s[0]
        dist = int(s[1:])
        out.append((dirc, dist))
    return out


def solve(rotations, start=50, mod=100):
    # Part 1: count times dial is exactly 0 at the end of a rotation
    pos = start % mod
    part1 = 0

    # Part 2: count every time a click causes dial to point at 0 (during rotations)
    part2 = 0

    for dirc, dist in rotations:
        # count intermediate hits of 0 during this rotation
        if dist > 0:
            if dirc == 'R':
                # need t in 1..dist with (pos + t) % mod == 0
                r = (-pos) % mod
                first_t = mod if r == 0 else r
            else:  # L
                # need t in 1..dist with (pos - t) % mod == 0 -> t ≡ pos (mod mod)
                r = pos % mod
                first_t = mod if r == 0 else r

            if first_t <= dist:
                part2 += 1 + (dist - first_t) // mod

        # update pos after the whole rotation
        if dirc == 'R':
            pos = (pos + dist) % mod
        else:
            pos = (pos - dist) % mod

        if pos % mod == 0:
            part1 += 1

    return part1, part2


def main(argv=None):
    opt = get_args()
    
    base = Path(__file__).parent
    fp = base / ('input.txt' if opt.submission else 'example_input.txt')

    if not fp.exists():
        # Try reading from stdin if data was piped
        if not sys.stdin.isatty():
            data = sys.stdin.read().splitlines()
        else:
            print(f'Input file not found: {fp}', file=sys.stderr)
            sys.exit(1)
    else:
        data = fp.read_text(encoding='utf-8').splitlines()

    rotations = parse_lines(data)
    
    with profile(opt.submission) as results:
        part1, part2 = solve(rotations)
        results["part1"] = part1
        results["part2"] = part2

    printr(part1, part2)


if __name__ == '__main__':
    main()