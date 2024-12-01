import os

from collections import Counter

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()

sample_input = """16
10
15
5
1
11
7
19
6
12
4"""


def solve(inputs, preamble=25):
    values = [int(line) for line in inputs.split("\n")]

    SEAT = 0
    DEVICE = max(values) + 3
    adapters = [DEVICE] + sorted(values, reverse=True) + [SEAT]

    diffs = [a - b for a, b in zip(adapters[:-1], adapters[1:])]
    print(f"Part 1: {Counter(diffs)[1] * Counter(diffs)[3]}")

    ways_from = {DEVICE: 1}
    for n, a in enumerate(adapters[1:], 1):
        next_in_reach = (next_a for next_a in adapters[:n] if next_a - a <= 3)
        ways_from[a] = sum(ways_from[next_a] for next_a in next_in_reach)
    print(f"Part 2: {ways_from[SEAT]}\n")


solve(sample_input, 5)
solve(actual_input)
