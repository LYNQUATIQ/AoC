import os
import re
from collections import defaultdict

from grid import XY
from utils import print_time_taken

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


@print_time_taken
def solve(inputs):
    vents1 = defaultdict(int)
    vents2 = defaultdict(int)
    for line in inputs.splitlines():
        x1, y1, x2, y2 = map(int, re.findall(r"\d+", line))
        start, end = XY(x1, y1), XY(x2, y2)
        straight_line = (start.x == end.x) ^ (start.y == end.y)
        unit_step = lambda s: s / abs(s) if s != 0 else 0
        step = XY(unit_step((end - start).x), unit_step((end - start).y))

        vents1[start] += straight_line
        vents2[start] += 1
        while start != end:
            start += step
            vents1[start] += straight_line
            vents2[start] += 1

    print(f"Part 1: {sum(c > 1 for c in vents1.values())}")
    print(f"Part 2: {sum(c > 1 for c in vents2.values())}\n")


solve(sample_input)
solve(actual_input)
