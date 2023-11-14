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


def solve(inputs: str, y_row: int) -> None:

    rotate = lambda x, y: (x + y, y - x)
    unrotate = lambda x, y: ((x - y) // 2, (x + y) // 2)

    y_row_left, y_row_right, beacons_on_y = set(), set(), set()
    regions: list[tuple[tuple[int, int], int]] = []
    for line in inputs.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
        distance = abs(sx - bx) + abs(sy - by)

        # For part 1... store the left/right extents as at row y
        if by == y_row:
            beacons_on_y.add(by)
        x_range_at_y = distance - abs(sy - y_row)
        if x_range_at_y >= 0:
            y_row_left.add(sx - x_range_at_y)
            y_row_right.add(sx + x_range_at_y)

        # For part 2... rotate the sensor regions by 45° and then look for gaps of 1
        north, south = (sx, sy - distance), (sx, sy + distance)
        (x1, y1), (x2, y2) = rotate(*north), rotate(*south)
        x, y = min(x1, x2), min(y1, y2)
        regions.append(((x, y), abs(x2 - x1) + 1))

    print(f"Part 1: { max(y_row_right) - min(y_row_left) + 1 - len(beacons_on_y)}")

    x_candidates, y_candidates = set(), set()
    for ((x1, y1), d1), ((x2, y2), d2) in combinations(regions, 2):
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
            break

    print(f"Part 2: {x * 4_000_000 + y}\n")


solve(sample_input, 10)
solve(actual_input, 2_000_000)
