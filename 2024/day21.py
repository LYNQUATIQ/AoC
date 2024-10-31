"""https://adventofcode.com/2024/day/21"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day21_input.txt")) as f:
    actual_input = f.read()


sample_input = """xxx"""


def solve(inputs: str):
    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}\n")


solve(sample_input)
# solve(actual_input)
