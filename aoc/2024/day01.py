"""https://adventofcode.com/2024/day/1"""

from collections import Counter
from aoc.download_aoc_inputs import get_input_data

actual_input = get_input_data(2024, 1)


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
