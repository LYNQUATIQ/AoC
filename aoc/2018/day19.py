"""https://adventofcode.com/2018/day/19"""

import os
import re

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day19_input.txt")) as f:
    actual_input = f.read()


OPERATIONS = {
    "addr": lambda p, r: r[p[0]] + r[p[1]],
    "addi": lambda p, r: r[p[0]] + p[1],
    "mulr": lambda p, r: r[p[0]] * r[p[1]],
    "muli": lambda p, r: r[p[0]] * p[1],
    "banr": lambda p, r: r[p[0]] & r[p[1]],
    "bani": lambda p, r: r[p[0]] & p[1],
    "borr": lambda p, r: r[p[0]] | r[p[1]],
    "bori": lambda p, r: r[p[0]] | p[1],
    "setr": lambda p, r: r[p[0]],
    "seti": lambda p, _: p[0],
    "gtir": lambda p, r: int(p[0] > r[p[1]]),
    "gtri": lambda p, r: int(r[p[0]] > p[1]),
    "gtrr": lambda p, r: int(r[p[0]] > r[p[1]]),
    "eqir": lambda p, r: int(p[0] == r[p[1]]),
    "eqri": lambda p, r: int(r[p[0]] == p[1]),
    "eqrr": lambda p, r: int(r[p[0]] == r[p[1]]),
}


@print_time_taken
def solve(inputs):
    ip_register, *program = inputs.splitlines()

    ip_register = int(ip_register[-1])
    instructions = [
        (line[:4], tuple(map(int, re.findall("\d+", line[4:])))) for line in program
    ]

    for part in (1, 2):
        registers, pointer = [part - 1, 0, 0, 0, 0, 0], 0
        while True:
            instruction, params = instructions[pointer]
            registers[ip_register] = pointer
            registers[params[2]] = OPERATIONS[instruction](params, registers)
            pointer = registers[ip_register]
            pointer += 1
            if pointer >= len(instructions) or (part == 2 and pointer == 1):
                break
        if part == 1:
            print(f"Part 1: {registers[0]}")

    n = registers[2]
    factor_sum = sum(i + n // i for i in range(1, int(n**0.5) + 1) if n % i == 0)
    print(f"Part 2: {factor_sum}\n")


solve(actual_input)
