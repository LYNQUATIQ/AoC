"""https://adventofcode.com/2023/day/23"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day23_input.txt")) as f:
    actual_input = f.read()


sample_input = """xxx"""


def solve(inputs):
    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}")


solve(sample_input)
# solve(actual_input)
