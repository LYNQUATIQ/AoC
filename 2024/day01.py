"""https://adventofcode.com/2024/day/1"""

import os
from collections import Counter

with open(os.path.join(os.path.dirname(__file__), "inputs/day01_input.txt")) as f:
    actual_input = f.read()


sample_input = """3   4
4   3
2   5
1   3
3   9
3   3
"""


def solve(inputs: str):
    list_a, list_b = [], []
    for line in inputs.splitlines():
        a, b = map(int, line.split())
        list_a.append(a)
        list_b.append(b)
    list_a, list_b = sorted(list_a), sorted(list_b)
    counts = Counter(list_b)
    distance, similarity = 0, 0
    for a, b in zip(list_a, list_b):
        distance += abs(a - b)
        similarity += a * counts[a]

    print(f"Part 1: {distance}")
    print(f"Part 2: {similarity}\n")


solve(sample_input)
solve(actual_input)
