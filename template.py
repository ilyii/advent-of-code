import argparse
import os


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def parse_input(args):
    """ Parse input """
    if args.submission:
        filepath = "input.txt"
    else:
        filepath = "example_input.txt"

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def printr(results):
    """ Print results """
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")

    print("--------------------")

if __name__ == "__main__":
    opt = get_args()
    data = parse_input(opt)


    # printr(opt, [result1, result2])
