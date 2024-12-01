"""https://adventofcode.com/2021/day/25"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day25_input.txt")) as f:
    actual_input = f.read()

sample_input = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""


def solve(inputs):
    east, south = set(), set()

    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            match c:
                case ">":
                    east.add((x, y))
                case "v":
                    south.add((x, y))

    width, height = x + 1, y + 1
    steps = 0
    while True:
        steps += 1
        moved = False
        new_east = set()
        for x, y in east:
            xy, target_xy = (x, y), ((x + 1) % width, y)
            if not (target_xy in east or target_xy in south):
                xy, moved = target_xy, True
            new_east.add(xy)
        east = new_east
        new_south = set()
        for x, y in south:
            xy, target_xy = (x, y), (x, (y + 1) % height)
            if not (target_xy in east or target_xy in south):
                xy, moved = target_xy, True
            new_south.add(xy)
        south = new_south
        if not moved:
            break

    print(f"Part 1: {steps}\n")


solve(sample_input)
solve(actual_input)
