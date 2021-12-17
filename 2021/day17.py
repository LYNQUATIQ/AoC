from collections import defaultdict
from itertools import product
from enum import Enum
import re

sample_input = """target area: x=20..30, y=-10..-5"""
actual_input = """target area: x=96..125, y=-144..-98"""


class Target:
    LONG = "Long"
    SHORT = "Short"
    HIT = "HIT!"

    def __init__(self, target_string) -> None:
        self.left, self.right, self.bottom, self.top = map(
            int,
            re.match(
                r"^target area: x=([-]?\d+)..([-]?\d+), y=([-]?\d+)..([-]?\d+)$",
                target_string,
            ).groups(),
        )

    def hit(self, x, y) -> bool:
        return self.left <= x <= self.right and self.bottom <= y <= self.top

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


def solve(inputs):
    target = Target(inputs)

    min_vx, max_vx = 1, target.right + 1
    min_vy, max_vy = target.bottom - 1, 0

    vy, best_height = 1, 0
    while True:
        vx = 1
        result = target.test_shot(vx, vy)
        while result != target.LONG and vx < max_vx:
            if result == target.HIT:
                max_vy = max(max_vy, vy + 1)
                best_height = max(best_height, (vy * (vy + 1)) // 2)
            vx += 1
            result = target.test_shot(vx, vy)
        vy += 1
        if vy > 20 * abs(target.top):
            break

    print(f"Part 1: {best_height}")

    valid_velocities = set()
    for vx, vy in product(range(min_vx, max_vx), range(min_vy, max_vy)):
        if target.test_shot(vx, vy) == Target.HIT:
            valid_velocities.add((vx, vy))
    print(f"Part 2: {len(valid_velocities)}")


solve(sample_input)
solve(actual_input)
