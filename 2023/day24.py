"""https://adventofcode.com/2023/day/24"""
import os
import re
from functools import cache
from itertools import combinations

with open(os.path.join(os.path.dirname(__file__), "inputs/day24_input.txt")) as f:
    actual_input = f.read()


sample_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


@cache
def intersect(x1, v1, x2, v2) -> bool:
    return True


XY_DIMENSIONS = (0, 1)


def solve(inputs: str, min_bound, max_bound):
    hailstones = []
    xy_coefficients = []  # stores (a, b) where y = ax + b
    for i, line in enumerate(inputs.splitlines()):
        x, y, z, vx, vy, vz = map(int, re.findall(r"-?\d+", line))
        a, b = (vy / vx, (y - (vy * x) / vx))
        hailstones.append(((x, y, z), (vx, vy, vz), (a, b)))
        xy_coefficients.append((vy / vx, (y - (vy * x) / vx), x, vx))

    intersections = 0
    for (a1, b1, x1, vx1), (a2, b2, x2, vx2) in combinations(xy_coefficients, 2):
        if a1 == a2:
            continue
        x = (b2 - b1) / (a1 - a2)
        y = x * a1 + b1
        if not ((min_bound <= x <= max_bound) and (min_bound <= y <= max_bound)):
            continue
        t1, t2 = (x - x1) / vx1, (x - x2) / vx2
        if t1 < 0 or t2 < 0:
            continue
        intersections += 1
    print(f"Part 1: {intersections}")
    return
    for (xyz1, vel1), (xyz2, vel2) in combinations(hailstones, 2):
        dimensions_to_check = []
        for d in XY_DIMENSIONS:
            if (vel1[d] != vel2[d]) and (xyz1[d] != xyz2[d]):
                dimensions_to_check.append(d)
        intersect_times = {
            (xyz2[d] - xyz1[d]) / (vel1[d] - vel2[d]) for d in dimensions_to_check
        }
        if len(intersect_times) != 1:
            continue
        t = intersect_times.pop()
        if t < 0:
            continue
        outside = not all(
            min_bound <= (xyz1[d] + vel1[d] * t) <= max_bound for d in XY_DIMENSIONS
        )
        if outside:
            continue

        intersections += 1

    print(f"Part 2: {False}\n")


solve(sample_input, 7, 27)
solve(actual_input, 200_000_000_000_000, 400_000_000_000_000)
