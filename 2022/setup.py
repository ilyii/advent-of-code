import sys
import os
import shutil

ROOT = "./days"

if __name__ == "__main__":
    day = int(sys.argv[1])
    os.mkdir(f"{ROOT}/day{day}")
    shutil.copyfile("./template.py", f"{ROOT}/day{day}/code.py")

    with open(f"{ROOT}/day{day}/input.txt", "w") as f:
        pass