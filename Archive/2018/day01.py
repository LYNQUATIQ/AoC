"""https://adventofcode.com/2018/day/1"""
import os

from itertools import cycle

with open(os.path.join(os.path.dirname(__file__), "inputs/day01_input.txt")) as f:
    actual_input = f.read()

sample_input = """+1
-2
+3
+1"""


def solve(inputs):
    values = list(map(int, inputs.splitlines()))

    print(f"Part 1: {sum(values)}")

    change = cycle(values)
    frequency, results = 0, set()
    while frequency not in results:
        results.add(frequency)
        frequency += next(change)

    print(f"Part 2: {frequency}\n")


solve(sample_input)
solve(actual_input)
