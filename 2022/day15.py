"""https://adventofcode.com/2022/day/15"""
from __future__ import annotations

import os
import re

from itertools import combinations, product

with open(os.path.join(os.path.dirname(__file__), f"inputs/day15_input.txt")) as f:
    actual_input = f.read()


sample_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def solve_part1(inputs: str, y_row: int, extent: int) -> int:
    no_beacons = set()
    beacons_on_y = 0
    for line in inputs.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
        if by == y_row:
            beacons_on_y += 1
        distance = abs(sx - bx) + abs(sy - by)
        x_range = distance - abs(sy - y_row)
        if x_range < 0:
            continue
        for x in range(-x_range, x_range + 1):
            no_beacons.add(sx + x)

    return len(no_beacons) - beacons_on_y


def solve_part2(inputs: str) -> int:

    rotate = lambda x, y: (x + y, y - x)
    unrotate = lambda x, y: ((x - y) // 2, (x + y) // 2)

    regions: list[tuple[tuple[int, int], int]] = []
    for line in inputs.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
        distance = abs(sx - bx) + abs(sy - by)
        north, south = (sx, sy - distance), (sx, sy + distance)
        (cx1, cy1), (cx2, cy2) = rotate(*north), rotate(*south)
        x, y = min(cx1, cx2), min(cy1, cy2)
        regions.append(((x, y), abs(cx2 - cx1) + 1))

    x_candidates, y_candidates = set(), set()
    for a, b in combinations(regions, 2):
        (x1, y1), d1 = a
        (x2, y2), d2 = b
        if x2 - (x1 + d1) == 1:
            x_candidates.add(x2 - 1)
        elif x1 - (x2 + d2) == 1:
            x_candidates.add(x1 - 1)
        if y2 - (y1 + d1) == 1:
            y_candidates.add(y2 - 1)
        elif y1 - (y2 + d2) == 1:
            y_candidates.add(y1 - 1)

    for x0, y0 in product(x_candidates, y_candidates):
        if not any(x <= x0 < x + d and y <= y0 < y + d for (x, y), d in regions):
            x, y = unrotate(x0, y0)
            return x * 4_000_000 + y

    raise ValueError


from utils import print_time_taken


@print_time_taken
def solve(inputs: str, y_row: int, extent: int) -> None:
    print(f"Part 1: {solve_part1(inputs,y_row, extent)}")
    print(f"Part 2: {solve_part2(inputs)}\n")


solve(sample_input, 10, 20)
solve(actual_input, 2_000_000, 4_000_000)
