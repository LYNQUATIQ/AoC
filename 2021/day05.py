import os
import re
from collections import defaultdict

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
        straight_line = (x1 == x2) ^ (y1 == y2)
        unit_step = lambda s: s / abs(s) if s != 0 else 0
        dx, dy = unit_step(x2 - x1), unit_step(y2 - y1)
        xy, end = (x1, y1), (x2, y2)
        while True:
            vents1[xy] += straight_line
            vents2[xy] += 1
            if xy == end:
                break
            xy = (xy[0] + dx, xy[1] + dy)

    print(f"Part 1: {sum(c > 1 for c in vents1.values())}")
    print(f"Part 2: {sum(c > 1 for c in vents2.values())}\n")


solve(sample_input)
solve(actual_input)
