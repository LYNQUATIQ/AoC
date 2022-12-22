"""https://adventofcode.com/2022/day/22"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

LEFT, RIGHT, UP, DOWN = (-1 + 0j, 1 + 0j, 0 - 1j, 0 + 1j)
FACING = {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}
TURN_ANTICLOCKWISE = {RIGHT: UP, UP: LEFT, LEFT: DOWN, DOWN: RIGHT}
TURN_CLOCKWISE = {RIGHT: DOWN, DOWN: LEFT, LEFT: UP, UP: RIGHT}
TURN = {"L": TURN_ANTICLOCKWISE, "R": TURN_CLOCKWISE}

VOID, WALL, OPEN = " ", "#", "."


def solve(inputs: str) -> None:
    map_data, instructions = inputs.split("\n\n")

    grid: dict[complex, str] = {}
    left_extent: list[int] = []
    right_extent: list[int] = []
    max_x = 0
    for y, row in enumerate(map_data.splitlines()):
        x = 0
        while row[x] == " ":
            x += 1
        left_extent.append(x)
        while x != " " and x < len(row):
            max_x = max(max_x, x)
            grid[complex(x, y)] = row[x]
            x += 1
        right_extent.append(x - 1)
    rows, columns = y + 1, max_x + 1

    xy, direction = complex(left_extent[0], 0), 1 + 0j
    ptr = 0
    finished = False
    while not finished:
        if instructions[ptr] in "LR":
            direction = TURN[instructions[ptr]][direction]
            ptr += 1
            continue
        steps = 0
        while instructions[ptr].isdigit():
            steps = steps * 10 + int(instructions[ptr])
            ptr += 1
            if ptr == len(instructions):
                finished = True
            if finished or not instructions[ptr].isdigit():
                break
        while steps:
            next_xy = xy + direction
            next_xy = complex(next_xy.real % columns, next_xy.imag % rows)
            while grid.get(next_xy, VOID) == VOID:
                next_xy += direction
                next_xy = complex(next_xy.real % columns, next_xy.imag % rows)
            if grid.get(next_xy) == WALL:
                break
            xy = next_xy
            steps -= 1

    x, y, facing = int(xy.real) + 1, int(xy.imag) + 1, FACING[direction]
    print(f"Part 1: {1000 * y + 4 *x + facing}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
