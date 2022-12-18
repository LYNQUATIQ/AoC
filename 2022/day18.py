"""https://adventofcode.com/2022/day/18"""
from __future__ import annotations

import os
import re

from collections import deque
from itertools import product

with open(os.path.join(os.path.dirname(__file__), f"inputs/day18_input.txt")) as f:
    actual_input = f.read()


sample_input = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

Cube = tuple[int, int, int]


def neighbours(cube: Cube, extent=999) -> set[Cube]:
    x, y, z = cube
    neighbours = set()
    if x >= 0:
        neighbours.add((x - 1, y, z))
    if x < extent:
        neighbours.add((x + 1, y, z))
    if y >= 0:
        neighbours.add((x, y - 1, z))
    if y < extent:
        neighbours.add((x, y + 1, z))
    if z >= 0:
        neighbours.add((x, y, z - 1))
    if z < extent:
        neighbours.add((x, y, z + 1))
    return neighbours


def solve(inputs: str) -> None:

    cubes = set()
    for line in inputs.splitlines():
        x, y, z = list(map(int, re.findall(r"\d+", line)))
        cubes.add((x, y, z))

    sides = 0
    for cube in cubes:
        for neighbour in neighbours(cube):
            sides += neighbour not in cubes
    print(f"Part 1: {sides}")

    extent = max(*(max(cube) for cube in cubes)) + 1

    open_air: set[Cube] = {(0, 0, 0)}
    queue: deque[Cube] = deque([(0, 0, 0)])
    while queue:
        xyz = queue.popleft()
        for next_xyz in neighbours(xyz, extent):
            if next_xyz not in cubes and next_xyz not in open_air:
                queue.append(next_xyz)
                open_air.add(next_xyz)

    gaps = set()
    for xyz in product(range(extent), range(extent), range(extent)):
        if not (xyz in cubes or xyz in open_air):
            gaps.add(xyz)

    for gap in gaps:
        for neighbour in neighbours(gap):
            sides -= neighbour in cubes

    print(f"Part 2: {sides}\n")


solve(sample_input)
solve(actual_input)
