"""https://adventofcode.com/2018/day/25"""
import os
import re

from collections import defaultdict
from itertools import combinations

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day25_input.txt")) as f:
    actual_input = f.read()

sample_input = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""


class Point(tuple):
    def __new__(cls, *_tuple):
        return tuple.__new__(cls, _tuple)

    def __add__(self, other):
        return type(self)(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return type(self)(*(a - b for a, b in zip(self, other)))


@print_time_taken
def solve(inputs):
    points = {Point(*map(int, (re.findall(r"-?\d+", l)))) for l in inputs.splitlines()}
    neighbours = defaultdict(list)
    for a, b in combinations(points, 2):
        if sum(map(abs, a - b)) <= 3:
            neighbours[a].append(b)

    constellations = {p: p for p in points}
    for point in points:
        my_constellation = constellations[point]
        for n in neighbours[point]:
            neighbours_constellation = constellations[n]
            if neighbours_constellation == my_constellation:
                continue
            for x in (
                p for p, c in constellations.items() if c == neighbours_constellation
            ):
                constellations[x] = my_constellation

    print(f"Part 1: {len(set(constellations.values()))}")


solve(sample_input)
solve(actual_input)
