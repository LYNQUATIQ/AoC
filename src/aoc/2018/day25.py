"""https://adventofcode.com/2018/day/25"""

import os
import re

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day25_input.txt")) as f:
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


@print_time_taken
def solve(inputs):
    points = [tuple(map(int, (re.findall(r"-?\d+", l)))) for l in inputs.splitlines()]
    constellations = {p: p for p in points}

    for i, point in enumerate(points[:-1]):
        my_constellation = constellations[point]
        for other in points[i + 1 :]:
            if sum(abs(a - b) for a, b in zip(point, other)) <= 3:
                neighbours_constellation = constellations[other]
                for merge in (
                    p
                    for p, c in constellations.items()
                    if c == neighbours_constellation
                ):
                    constellations[merge] = my_constellation

    print(f"Part 1: {len(set(constellations.values()))}")


solve(sample_input)
solve(actual_input)
