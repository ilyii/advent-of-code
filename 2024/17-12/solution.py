import argparse
import os
from numbers import Number
import re
from typing import Any, Tuple


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
    

def step(registers, program, pc, out):
    """
    Program logic.
    """
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
    instruction_pointer = 0
    out = []
    while instruction_pointer < len(program):
        registers, instruction_pointer, out = step(registers, program, instruction_pointer, out)
    return out


def submission(data:Any) -> Tuple[Number, Number]:
    registers, program = data

    # Part 1
    part_1 = ','.join([str(x) for x in compute(registers, program)])

    # Part 2
    # - The program depends on A, iteratively shifted by 3 bits (divided by 8).

    possibilities = {0: [x for x in range(8)]}
    for exponent in range(1, len(program)):
        possibilities[exponent] = []
        for p in possibilities[exponent - 1]:
            for q in range(8):
                ra = 8 * p + q
                registers[0] = ra
                out = compute(registers, program)
                l = len(out)
                if out == program[len(program) - l:]:
                    possibilities[exponent].append(ra)
                if out == program:
                    part_2 = ra

    return part_1, part_2

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
    result1, result2 = submission(data)

    # ---- OUTPUT ---- #
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

    # import timeit
    # res = timeit.timeit(lambda: submission(data), number=10)
    # print(f"Time: {res/10:.7f}s")