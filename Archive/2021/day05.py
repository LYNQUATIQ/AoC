"""https://adventofcode.com/2021/day/5"""
import os
import re
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), f"inputs/day05_input.txt")) as f:
    actual_input = f.read()

sample_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


def solve(inputs):
    unit_step = lambda s: -1 if s < 0 else s > 0
    vents1 = defaultdict(int)
    vents2 = defaultdict(int)

    for line in inputs.splitlines():
        x, y, end_x, end_y = map(int, re.findall(r"\d+", line))
        dx, dy = unit_step(end_x - x), unit_step(end_y - y)
        straight_line = (x == end_x) ^ (y == end_y)
        while True:
            vents1[(x, y)] += straight_line
            vents2[(x, y)] += 1
            if (x, y) == (end_x, end_y):
                break
            x, y = x + dx, y + dy

    print(f"Part 1: {sum(c > 1 for c in vents1.values())}")
    print(f"Part 2: {sum(c > 1 for c in vents2.values())}\n")


solve(sample_input)
solve(actual_input)
