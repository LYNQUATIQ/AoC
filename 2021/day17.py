from collections import defaultdict
from itertools import product
from enum import Enum
import re

sample_input = """target area: x=20..30, y=-10..-5"""
actual_input = """target area: x=96..125, y=-144..-98"""


def solve(inputs):

    left, right, bottom, top = map(int, re.findall(r"-?\d+", inputs))

    # The highest shot will be the one that hits the water and in the next step hits the
    # bottom. It hits the water at the same velocity it rose at so the velocity needs to
    # equal the (absolute) depth (and will also be the maximum velocity)

    min_vx, max_vx = 1, right
    min_vy, max_vy = bottom, abs(bottom)

    print(f"Part 1: {sum(range(max_vy))}")

    def test_shot(self, vx, vy):
        x, y = 0, 0
        while y >= self.bottom:
            x, y = x + vx, y + vy
            vx = max(vx + (1 if x < 0 else -1 if x > 0 else 0), 0)
            vy -= 1
            if self.hit(x, y):
                return self.HIT
        if x < self.left:
            return self.SHORT
        return self.LONG

    valid_velocities = set()
    for vx0, vy0 in product(range(min_vx, max_vx + 1), range(min_vy, max_vy + 1)):
        x, y, vx, vy = 0, 0, vx0, vy0
        while y >= bottom:
            x, y = x + vx, y + vy
            if left <= x <= right and bottom <= y <= top:
                valid_velocities.add((vx0, vy0))
            vx, vy = max(vx - 1, 0), vy - 1

    print(f"Part 2: {len(valid_velocities)}\n")


solve(sample_input)
solve(actual_input)
