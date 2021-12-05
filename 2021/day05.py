import os

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
    grid1 = defaultdict(int)
    grid2 = defaultdict(int)
    for line in inputs.splitlines():
        a, b = line.split(" -> ")
        start, end = XY(*map(int, a.split(","))), XY(*map(int, b.split(",")))
        straight_line = (start.x == end.x) ^ (start.y == end.y)
        grid1[start] += straight_line
        grid2[start] += 1

        unit_step = lambda s: s / abs(s) if s != 0 else 0
        step = XY(unit_step((end - start).x), unit_step((end - start).y))
        while start != end:
            start += step
            grid1[start] += straight_line
            grid2[start] += 1

    print(f"Part 1: {len([c for c in grid1.values() if c > 1])}")
    print(f"Part 2: {len([c for c in grid2.values() if c > 1])}\n")


solve(sample_input)
solve(actual_input)
