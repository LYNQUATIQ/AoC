"""https://adventofcode.com/2023/day/22"""
import os
import re

from itertools import product

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


def print_state(space):
    print(" x")
    for z in range(10, 0, -1):
        row = ""
        for x in range(3):
            c = "."
            for y in range(3):
                b = space.get((x, y, z))
                if b is not None:
                    if c == ".":
                        c = b
                    else:
                        if c != b:
                            c = "?"
            row += c
        print(row, z)
    print("--- 0")
    print()
    print(" y")
    for z in range(10, 0, -1):
        row = ""
        for y in range(3):
            c = "."
            for x in range(3):
                b = space.get((x, y, z))
                if b is not None:
                    if c == ".":
                        c = b
                    else:
                        if c != b:
                            c = "?"
            row += c
        print(row, z)
    print("--- 0")
    print()


def find_falling_brick(space, bricks, brick_to_ignore=None):
    for brick_id, (footprint, _, z0) in bricks.items():
        if z0 == 1:
            continue
        can_fall = True
        for x, y in footprint:
            below = space.get((x, y, z0 - 1))
            if below is not None and below != brick_to_ignore:
                can_fall = False
                break
        if can_fall:
            return brick_id
    return None


@print_time_taken
def solve(inputs: str):
    bricks = {}
    space = {}
    for i, line in enumerate(inputs.splitlines()):
        x0, y0, z0, x1, y1, z1 = map(int, re.findall(r"\d+", line))
        brick_id = chr(65 + i)
        bricks[brick_id] = (x0, y0, z0, x1, y1, z1)
        footprint = {xy for xy in product(range(x0, x1 + 1), range(y0, y1 + 1))}
        z_extent = z1 - z0 + 1
        bricks[brick_id] = (footprint, z_extent, z0)
        for x, y in footprint:
            for h in range(z_extent):
                space[(x, y, z0 + h)] = brick_id

    while brick_id := find_falling_brick(space, bricks):
        footprint, z_extent, z0 = bricks[brick_id]
        bricks[brick_id] = (footprint, z_extent, z0 - 1)
        for x, y in footprint:
            space[(x, y, z0 - 1)] = brick_id
            del space[(x, y, z0 + z_extent - 1)]

    can_delete = set()
    for brick_id in bricks:
        if find_falling_brick(space, bricks, brick_id) is None:
            can_delete.add(brick_id)

    print(f"Part 1: {len(can_delete)}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
