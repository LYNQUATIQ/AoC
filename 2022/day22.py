"""https://adventofcode.com/2022/day/22"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """xxx"""


def solve(inputs: str) -> None:
    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}\n")


solve(sample_input)
# solve(actual_input)
