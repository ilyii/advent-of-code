import argparse
import os
import sys
from numbers import Number
import re
from typing import Any, Tuple

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """ Argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def combo(operand, registers):
    """
    Helper to get combo value.
    """
    if operand <= 3:
        return operand
    if operand <= 6:
        return registers[operand - 4]
    

def step(registers, program, pc):
    """
    Program logic.
    """
    out = []
    opcode = program[pc]
    operand = program[pc + 1]
    combo_operand = combo(operand, registers)
    if opcode == 0:
        registers[0] = int(registers[0] / 2 ** combo_operand)
    elif opcode == 1:
        registers[1] = registers[1] ^ operand
    elif opcode == 2:
        registers[1] = combo_operand % 8
    elif opcode == 3 and registers[0] != 0:
        pc = operand
        return registers, pc, out
    elif opcode == 4:
        registers[1] = registers[1] ^ registers[2]
    elif opcode == 5:
        out.append(combo_operand % 8)
    elif opcode == 6:
        registers[1] = int(registers[0] / 2 ** combo_operand)
    elif opcode == 7:
        registers[2] = int(registers[0] / 2 ** combo_operand)
    pc += 2
    return registers, pc, out


def compute(registers, program):
    """
    Run the program.
    """



def submission(data:Any) -> Tuple[Number, Number]:
    registers, program = data

    # Part 1
    part_1 = []
    pc = 0
    while pc < len(program):
        registers, pc, o = step(registers, program, pc)
        part_1.extend(o)
    
    # Part 2
    # - The program depends on A, iteratively shifted by 3 bits (divided by 8).

    def find(program, reg, pc):
        if abs(pc) > len(program): 
            return reg[0]
        for i in range(8):
            digit = step([(reg[0] * 8) + i, reg[1], reg[2]],program, pc)[0]
            if digit == program[pc]:
                e = find(program, [reg[0] * 8 + i, reg[1], reg[2]], pc - 1)
                if e: 
                    return e

    part_2 = find(program, [0, registers[1], registers[2]], -1)

    return ",".join(map(str, part_1)), part_2

if __name__ == "__main__":
    opt = get_args()

    if opt.submission:
        inputpath = "input.txt"
    else:
        inputpath = "example_input.txt"

    # ---- INPUT PROCESSING ---- # 
    with open(inputpath, "r", encoding="utf-8") as f:
        data = f.read()
    register_values = list(map(int, re.findall(r"\d+", data.split("\n\n")[0])))
    program = list(map(int, re.findall(r"\d+", data.split("\n\n")[1])))

    data = (register_values, program)
    
    # ---- SUBMISSION ---- #
    with profile(opt.submission) as results:
        result1, result2 = submission(data)
        results["part1"] = result1
        results["part2"] = result2

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")