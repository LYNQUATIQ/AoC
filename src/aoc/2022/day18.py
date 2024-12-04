"""https://adventofcode.com/2022/day/18"""

from __future__ import annotations

import os
import re

from collections import deque
from itertools import product

with open(os.path.join(os.path.dirname(__file__), "inputs/day18_input.txt")) as f:
    actual_input = f.read()


example_input = """2,2,2
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


def neighbours(xyz: tuple[int, int, int], span: int = 999) -> set[tuple[int, int, int]]:
    x, y, z = xyz
    neighbours = set()
    if x >= 0:
        neighbours.add((x - 1, y, z))
    if x < span:
        neighbours.add((x + 1, y, z))
    if y >= 0:
        neighbours.add((x, y - 1, z))
    if y < span:
        neighbours.add((x, y + 1, z))
    if z >= 0:
        neighbours.add((x, y, z - 1))
    if z < span:
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

    max_span = max(*(max(cube) for cube in cubes)) + 1
    open_air: set[tuple[int, int, int]] = {(0, 0, 0)}
    queue: deque[tuple[int, int, int]] = deque([(0, 0, 0)])
    while queue:
        xyz = queue.popleft()
        for next_xyz in neighbours(xyz, max_span):
            if next_xyz in cubes or next_xyz in open_air:
                continue
            open_air.add(next_xyz)
            queue.append(next_xyz)

    for xyz in product(range(max_span), range(max_span), range(max_span)):
        if not (xyz in cubes or xyz in open_air):
            for neighbour in neighbours(xyz):
                sides -= neighbour in cubes
    print(f"Part 2: {sides}\n")


solve(example_input)
solve(actual_input)
