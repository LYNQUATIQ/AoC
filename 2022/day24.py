"""https://adventofcode.com/2022/day/24"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day24_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """xxx"""


def solve(inputs: str) -> None:
    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}")


solve(SAMPLE_INPUT)
# solve(actual_input)
