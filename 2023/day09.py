"""https://adventofcode.com/2023/day/9"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day09_input.txt")) as f:
    actual_input = f.read()


sample_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def extrapolate(values: list[int], back: bool = False) -> int:
    if all(n == 0 for n in values):
        return 0
    x = extrapolate([b - a for a, b in zip(values[:-1], values[1:])], back)
    return values[0] - x if back else values[-1] + x


def solve(inputs):
    histories = [[int(n) for n in line.split()] for line in inputs.splitlines()]
    print(f"Part 1: {sum(extrapolate(values) for values in histories)}")
    print(f"Part 2: {sum(extrapolate(values, back=True) for values in histories)}\n")


solve(sample_input)
solve(actual_input)
