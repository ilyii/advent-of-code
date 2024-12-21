import argparse
from collections import Counter, defaultdict
from functools import cache
import os
import re



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

# <CUSTOM>    
"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
# </CUSTOM>
if __name__ == "__main__":
    opt = get_args()
    data = read(opt)
    data = [line.strip() for line in data]

    keyp = {c: (i % 3, i // 3) for i, c in enumerate("789456123 0A")}
    dirp = {c: (i % 3, i // 3) for i, c in enumerate(" ^A<v>")}

    # x=Imag, y=Real
    NUMPAD = {c: i + 1j * j
                for i, line in enumerate("789\n456\n123\n 0A".splitlines())
                for j, c in enumerate(line)}
    REMOTEPAD = {c: i + 1j * j
                    for i, line in enumerate(" ^A<v>")
                    for j, c in enumerate(line)}


    def translate(G: dict[complex, str], s: str, i=1):
        px, py = G['A'].real, G['A'].imag
        bx, by = G[" "].real, G[" "].imag
        res = Counter()
        for c in s:
            nx, ny = G[c].real, G[c].imag
            f = nx == bx and py == by or ny == by and px == bx
            res[(nx-px + 1j*(ny-py), f)] += i
            px, py = nx, ny
        return res


    part_1 = part_2 = 0
    for code in data:
        res = translate(NUMPAD, code)
        for idx in range(25+1):
            res = sum((translate(REMOTEPAD, 
                                ("<" * int(-c.imag) + "v" * int(c.real) + "^" * int(-c.real) + ">" * int(c.imag))[:: -1 if f else 1] + "A", res[(c, f)]) for c, f in res), Counter())   
            if idx < 2:
                part_1 += res.total() * int(code[:3])
            
            part_2 += res.total() * int(code[:3])
    printr([part_1, part_2])