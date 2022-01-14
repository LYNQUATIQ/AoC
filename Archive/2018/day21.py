"""https://adventofcode.com/2018/day/21"""
import os

from itertools import cycle

with open(os.path.join(os.path.dirname(__file__), f"inputs/day21_input.txt")) as f:
    actual_input = f.read()


def solve(inputs):
    instructions = inputs.splitlines()
    seed = int(instructions[8].split()[1])
    multiplier = int(instructions[12].split()[2])

    b = 0
    possible_answers = set()
    while True:
        a = b | 0x10000
        b = seed
        while True:
            b += a & 0xFF
            b *= multiplier
            b &= 0xFFFFFF
            if a < 256:
                if not possible_answers:
                    print(f"Part 1: {b}")
                if b in possible_answers:
                    print(f"Part 2: {last_unseen_answer}")
                    return
                last_unseen_answer = b
                possible_answers.add(b)
                break
            else:
                a = a // 256


solve(actual_input)
