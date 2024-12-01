"""https://adventofcode.com/2021/day/1"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day01_input.txt")) as f:
    actual_input = f.read()

sample_input = """199
200
208
210
200
207
240
269
260
263"""


def solve(inputs):
    values = tuple(map(int, inputs.splitlines()))
    print(f"Part 1: {sum(a < b for a, b in zip(values, values[1:]))}")
    print(f"Part 2: {sum(a < b for a, b in zip(values, values[3:]))}\n")


solve(sample_input)
solve(actual_input)
