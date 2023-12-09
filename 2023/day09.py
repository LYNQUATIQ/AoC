"""https://adventofcode.com/2023/day/9"""
import os
import re

with open(os.path.join(os.path.dirname(__file__), "inputs/day09_input.txt")) as f:
    actual_input = f.read()


sample_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def extrapolate(values: list[int], backwards: bool = False) -> int:
    if all(n == 0 for n in values):
        return 0
    differences = [b - a for a, b in zip(values[:-1], values[1:])]
    x = extrapolate(differences, backwards)
    return values[0] - x if backwards else values[-1] + x


def solve(inputs):
    total1, total2 = 0, 0
    for line in inputs.splitlines():
        values = [int(n) for n in line.split()]
        total1 += extrapolate(values)
        total2 += extrapolate(values, backwards=True)

    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}\n")


solve(sample_input)
solve(actual_input)
