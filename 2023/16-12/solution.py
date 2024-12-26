import argparse
import os


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


if __name__ == "__main__":
    opt = get_args()
    data = read(opt)

    G = {complex(i,j): char 
         for j, row in enumerate(data) # Row: Real
         for i, char in enumerate(row.strip())} # Column: Imaginary

    print(read(opt).read())
    print(G)


    def process(t):
        stack = [t]
        visited = set()
        while stack:
            pos, d = stack.pop()
            while not (pos, d) in visited:
                visited.add((pos, d))
                pos += d
                if G.get(pos) == "|":
                    d = 0+1j
                    stack.append((pos, -d))

                elif G.get(pos) == "-":
                    d = 1+0j
                    stack.append((pos, -d))

                elif G.get(pos) == "/":
                    d = -complex(d.imag, d.real) # turn 90 degrees left
                elif G.get(pos) == "\\":
                    d = complex(d.imag, d.real) # turn 90 degrees right
                elif G.get(pos) is None: # Out of bounds
                    break

        return len(set(p for p, _ in visited)) - 1

    start = -1+0j # left outside
    d = 1+0j # right
    part_1 = process((start, d))

    part_2 = max(map(process, ((pos-d, d) for d in (1,1j,-1,-1j)
                            for pos in G if pos-d not in G)))

    printr([part_1, part_2])
