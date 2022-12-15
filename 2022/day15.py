"""https://adventofcode.com/2022/day/15"""
from __future__ import annotations

import os
import re

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

from typing import NamedTuple


class XY(NamedTuple):
    x: int
    y: int

    def x_distance(self, other: XY) -> int:
        return abs(self.x - other.x)

    def y_distance(self, other: XY) -> int:
        return abs(self.y - other.y)

    def distance(self, other: XY) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


from itertools import product

sensors: dict[XY, XY] = {}


def check_row(y: int) -> int:
    no_beacons = set()
    beacons = set()
    for s, b in sensors.items():
        if s.distance(b) < s.distance(XY(s.x, y)):
            continue
        if b.y == y:
            beacons.add(b)
        x_range = s.distance(b) - abs(s.y - y)
        for x in range(-x_range, x_range + 1):
            no_beacons.add(s.x + x)

    return len(no_beacons) - len(beacons)


from utils import print_time_taken
from collections import deque

import numpy as np


@print_time_taken
def solve(inputs: str, y_row: int, extent: int) -> None:

    space = np.ones((extent + 1, extent + 1), dtype=bool)
    for line in inputs.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))

        sensor, beacon = XY(sx, sy), XY(bx, by)
        d = sensor.distance(beacon)
        # try:
        #     space[by, bx] = 0
        # except IndexError:
        #     pass
        # try:
        #     space[sy, sx] = 1
        # except IndexError:
        #     pass

        for y in range(max(0, sensor.y - d), min(sensor.y + d + 1, extent + 1)):
            x_length = sensor.distance(beacon) - abs(sensor.y - y)
            assert 0 <= x_length <= sensor.distance(beacon)
            for x in range(sensor.x - x_length, sensor.x + x_length + 1):
                if 0 <= x <= extent:
                    space[y, x] = 0

    # for i, row in enumerate(space):
    #     print("".join(c for c in space[i]))

    # print(f"Part 1: {check_row(y_row)}")
    y, x = np.where(space == 1)
    print(x, y)
    print(f"Part 2: {x* 4_000_000 + y}\n")


solve(sample_input, 10, 20)
solve(actual_input, 2_000_000, 4_000_000)
