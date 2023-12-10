"""https://adventofcode.com/2023/day/10"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()


sample_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


START = "S"
NORTH, SOUTH, EAST, WEST = -1j, +1j, 1, -1
DIRECTIONS = {
    (NORTH, "|"): NORTH,
    (SOUTH, "|"): SOUTH,
    (EAST, "-"): EAST,
    (WEST, "-"): WEST,
    (SOUTH, "L"): EAST,
    (WEST, "L"): NORTH,
    (SOUTH, "J"): WEST,
    (EAST, "J"): NORTH,
    (EAST, "7"): SOUTH,
    (NORTH, "7"): WEST,
    (WEST, "F"): SOUTH,
    (NORTH, "F"): EAST,
}


def solve(inputs):
    grid: dict[complex, str] = {}
    start: complex | None = None
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            grid[complex(x, y)] = c
            if c == START:
                start = complex(x, y)
    assert start

    valid_headings = {
        heading
        for heading in (NORTH, SOUTH, EAST, WEST)
        if (heading, grid.get(start + heading)) in DIRECTIONS
    }

    direction = valid_headings.pop()
    location, steps = start + direction, 1
    while location != start:
        direction = DIRECTIONS[direction, grid[location]]
        location += direction
        steps += 1

    print(f"Part 1: {steps//2}")
    print(f"Part 2: {False}\n")


solve(sample_input)
solve(actual_input)
