"""https://adventofcode.com/2023/day/24"""
import os
import re

import numpy as np

from itertools import combinations

with open(os.path.join(os.path.dirname(__file__), "inputs/day24_input.txt")) as f:
    actual_input = f.read()


sample_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


def solve(inputs: str, min_bound, max_bound):
    hailstones = []
    xy_coefficients = []
    for i, line in enumerate(inputs.splitlines()):
        x, y, z, vx, vy, vz = map(int, re.findall(r"-?\d+", line))
        hailstones.append(((x, y, z), (vx, vy, vz)))
        # Store coeffients for formula: y = ax + b, along with x, vx (to convert x->t)
        a, b = vy / vx, y - (vy * x) / vx
        xy_coefficients.append((a, b, x, vx))

    intersections = 0
    for (a1, b1, x1, vx1), (a2, b2, x2, vx2) in combinations(xy_coefficients, 2):
        if a1 == a2:
            continue  # Never intersect - moving in parallel
        x = (b2 - b1) / (a1 - a2)
        y = x * a1 + b1
        if not ((min_bound <= x <= max_bound) and (min_bound <= y <= max_bound)):
            continue  # Intersect outside of the test area
        if (x - x1) / vx1 < 0 or (x - x2) / vx2 < 0:
            continue  # Intersected in the past
        intersections += 1
    print(f"Part 1: {intersections}")

    # Assume rock is at position xyz_rock with velocity vel_rock
    # Each hailstone is at position xyz_i and vel_i (where i is the hailstone index)
    #
    # We know that the rock and hailstone i will intersect at some time time_i
    #    xyz_rock + time_i * vel_rock = xyz_i + time_i * vel_i
    #    (xyx_rock - xyz_i) = time_i * (vel_i - vel_rock)
    #
    # Take the product of both sides with (vel_rock - vel_i) => 0 on the RHS
    #    (xyx_rock - xyz_i) * (vel_rock - vel_i) = 0
    #
    # We can now take *any* three rocks (a, b , and c) and use the above equation to
    # get 9 equations with 6 unknowns (the three dimensions of xyz_rock and vel_rock).
    # We can rearrange them into 6 equations by taking the differences between each
    # pair of hailstones.
    #
    # We can then use numpy to solve these six equantions for xyz_rock and vel_rock

    (x0, y0, z0), (vx0, vy0, vz0) = hailstones[0]
    (x1, y1, z1), (vx1, vy1, vz1) = hailstones[1]
    (x2, y2, z2), (vx2, vy2, vz2) = hailstones[2]

    coefficients = np.array(
        [
            [vy1 - vy0, vx0 - vx1, 0, y0 - y1, x1 - x0, 0],
            [vy2 - vy0, vx0 - vx2, 0, y0 - y2, x2 - x0, 0],
            [vz1 - vz0, 0, vx0 - vx1, z0 - z1, 0, x1 - x0],
            [vz2 - vz0, 0, vx0 - vx2, z0 - z2, 0, x2 - x0],
            [0, vz1 - vz0, vy0 - vy1, 0, z0 - z1, y1 - y0],
            [0, vz2 - vz0, vy0 - vy2, 0, z0 - z2, y2 - y0],
        ]
    )

    x = [
        (y0 * vx0 - y1 * vx1) - (x0 * vy0 - x1 * vy1),
        (y0 * vx0 - y2 * vx2) - (x0 * vy0 - x2 * vy2),
        (z0 * vx0 - z1 * vx1) - (x0 * vz0 - x1 * vz1),
        (z0 * vx0 - z2 * vx2) - (x0 * vz0 - x2 * vz2),
        (z0 * vy0 - z1 * vy1) - (y0 * vz0 - y1 * vz1),
        (z0 * vy0 - z2 * vy2) - (y0 * vz0 - y2 * vz2),
    ]

    xyz_rock = tuple(int(i) for i in np.linalg.solve(coefficients, x)[:3])

    print(f"Part 2: {sum(xyz_rock)}\n")


solve(sample_input, 7, 27)
solve(actual_input, 200_000_000_000_000, 400_000_000_000_000)
