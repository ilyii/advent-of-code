import argparse
import os
from numbers import Number
from typing import Any, Tuple



def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()

def submission(data:Any) -> Tuple[Number, Number]:
    """ Logic """
    visited = set()
    head = 0
    tail = 0
    dirs = {'L':+1, 'R':-1, 'D':1j, 'U':-1j}
    sign = lambda x: complex((x.real>0) - (x.real<0), (x.imag>0) - (x.imag<0))
    for idx, (d, n) in enumerate(data):
        for _ in range(n):
            head += dirs[d]
            dist = head - tail
            if abs(dist) > 1:
                print(dist, sign(dist))
                tail += sign(dist)
                visited.add(tail)

    return len(visited),0



    


if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read().splitlines()
    
    data = [(str(x.split()[0]), int(x.split()[1])) for x in data]
    print(data)

    
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