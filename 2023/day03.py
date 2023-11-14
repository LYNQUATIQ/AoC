"""https://adventofcode.com/2023/day/3"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day03_input.txt")) as f:
    actual_input = f.read()


sample_input = """xxx"""


def solve(inputs):
    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}")


solve(sample_input)
# solve(actual_input)
