"""https://adventofcode.com/2018/day/16"""

import os
import re

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day16_input.txt")) as f:
    actual_input = f.read()


example_input = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]



"""

OPERATIONS = {
    "addr": lambda p, r: r[p[1]] + r[p[2]],
    "addi": lambda p, r: r[p[1]] + p[2],
    "mulr": lambda p, r: r[p[1]] * r[p[2]],
    "muli": lambda p, r: r[p[1]] * p[2],
    "banr": lambda p, r: r[p[1]] & r[p[2]],
    "bani": lambda p, r: r[p[1]] & p[2],
    "borr": lambda p, r: r[p[1]] | r[p[2]],
    "bori": lambda p, r: r[p[1]] | p[2],
    "setr": lambda p, r: r[p[1]],
    "seti": lambda p, r: p[1],
    "gtir": lambda p, r: int(p[1] > r[p[2]]),
    "gtri": lambda p, r: int(r[p[1]] > p[2]),
    "gtrr": lambda p, r: int(r[p[1]] > r[p[2]]),
    "eqir": lambda p, r: int(p[1] == r[p[2]]),
    "eqri": lambda p, r: int(r[p[1]] == p[2]),
    "eqrr": lambda p, r: int(r[p[1]] == r[p[2]]),
}


class Sample:
    def __init__(self, before, instruction, after) -> None:
        self.before, self.instruction, self.after = before, instruction, after
        self.op_code = self.instruction[0]
        self.candidates = set()
        for operation, fn in OPERATIONS.items():
            registers = before[:]
            registers[instruction[3]] = fn(instruction, before)
            if registers == after:
                self.candidates.add(operation)


@print_time_taken
def solve(inputs):
    sample_inputs, program = inputs.split("\n\n\n\n")

    samples = [
        Sample(*(map(lambda x: list(map(int, re.findall("\d+", x))), s.splitlines())))
        for s in sample_inputs.split("\n\n")
    ]
    print(f"Part 1: {sum(len(s.candidates)>=3 for s in samples)}")

    op_codes, candidates = {}, {opcode: set(OPERATIONS) for opcode in range(16)}
    for sample in samples:
        candidates[sample.op_code] &= sample.candidates

    while resolved_condidates := [o for o, c in candidates.items() if len(c) == 1]:
        op_code = resolved_condidates[0]
        operation = candidates.pop(op_code).pop()
        op_codes[op_code] = operation
        for candidate_set in candidates.values():
            candidate_set.discard(operation)

    registers = [0, 0, 0, 0]
    for params in (list(map(int, re.findall("\d+", l))) for l in program.splitlines()):
        registers[params[3]] = OPERATIONS[op_codes[params[0]]](params, registers)

    print(f"Part 2: {registers[0]}\n")


solve(example_input)
solve(actual_input)
