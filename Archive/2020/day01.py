import os

from itertools import combinations

with open(os.path.join(os.path.dirname(__file__), "inputs/day01_input.txt")) as f:
    actual_input = f.read()

sample_input = """1721
979
366
299
675
1456"""


def solve(inputs):
    values = [int(value) for value in inputs.split("\n")]

    for a, b in combinations(values, 2):
        if a + b == 2020:
            print(f"Part 1: {a * b}")
            break

    for a, b, c in combinations(values, 3):
        if a + b + c == 2020:
            print(f"Part 2: {a * b * c}\n")
            break


solve(sample_input)
solve(actual_input)
