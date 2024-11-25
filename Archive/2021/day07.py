"""https://adventofcode.com/2021/day/7"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day07_input.txt")) as f:
    actual_input = f.read()

sample_input = """16,1,2,0,4,2,7,1,2,14"""


def solve(inputs):
    positions = tuple(map(int, inputs.split(",")))
    part1, part2 = set(), set()
    for x in range(min(positions), max(positions) + 1):
        distances = tuple(abs(x - p) for p in positions)
        part1.add(sum(distances))
        part2.add(sum(d * (d + 1) // 2 for d in distances))

    print(f"Part 1: {min(part1)}")
    print(f"Part 2: {min(part2)}\n")


solve(sample_input)
solve(actual_input)

from intcode_computer import IntCodeComputer

computer = IntCodeComputer(map(int, actual_input.split(",")))
computer.run_program()
print(computer.ascii_output())
