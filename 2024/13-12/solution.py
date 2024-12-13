import argparse
from collections import defaultdict
import os
import re
from numbers import Number
from typing import Any, Tuple



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def submission(data:Any) -> Tuple[Number, Number]:
    """ Logic 
    
    Thoughts: 
    - Each machine can have [0,inf) solutions.
    - 

    """

    # (xa xb) (i) _ (xp)
    # (ya yb) (j) - (yp)
    for part in range(1,3):
        costs = 0
        for _,machine in enumerate(data):
            xa, ya, xb, yb, xp, yp = map(int, machine)
            if part == 2:
                xp, yp = xp + 10000000000000, yp + 10000000000000

            det = (xa*yb - xb*ya)
            if det == 0:
                continue

            num_m = yb * xp - xb * yp 
            if num_m % det != 0:
                continue

            m = num_m // det
            if m < 0:
                continue

            num_n = xa * yp - ya * xp
            if num_n % det != 0:
                continue

            n = num_n // det
            if n < 0:
                continue

            costs += 3 * m + n

        yield costs


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read().split("\n\n")

    data = [re.findall(r'\d+', obj) for obj in data]
    # ---- SUBMISSION ---- #
    result1, result2 = submission(data)
    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

    import timeit
    res = timeit.timeit(lambda: submission(data), number=10)
    print(f"Time: {res/10:.7f}s")