import os

from collections import defaultdict
from itertools import combinations

with open(os.path.join(os.path.dirname(__file__), f"inputs/day17_input.txt")) as f:
    actual_input = f.read()

TARGET = 150


def solve(inputs):
    containers = [int(line) for line in inputs.splitlines()]

    good_combos = defaultdict(int)
    for i in range(1, len(containers) + 1):
        for combo in combinations(containers, i):
            if sum(combo) == TARGET:
                good_combos[len(combo)] += 1

    print(f"Part 1: {sum(good_combos.values())}")
    print(f"Part 2: {good_combos[min(good_combos.keys())]}\n")


solve(actual_input)