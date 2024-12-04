"""https://adventofcode.com/2023/day/10"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()


example_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


START = "S"
NORTH, SOUTH, EAST, WEST = -1j, +1j, 1, -1
PIPES = {
    (NORTH, SOUTH): "|",
    (NORTH, EAST): "L",
    (NORTH, WEST): "J",
    (SOUTH, EAST): "F",
    (SOUTH, WEST): "7",
    (EAST, WEST): "-",
}
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


def solve(inputs: str):
    grid: dict[complex, str] = {}
    start: complex | None = None
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            grid[complex(x, y)] = c
            if c == START:
                start = complex(x, y)
    width, height = x + 1, y + 1

    start_headings = tuple(
        h for h in (NORTH, SOUTH, EAST, WEST) if (h, grid.get(start + h)) in DIRECTIONS
    )
    grid[start] = PIPES[start_headings]

    direction = start_headings[0]
    pipe_path, location = {start}, start
    while (location := location + direction) != start:
        pipe_path.add(location)
        direction = DIRECTIONS[direction, grid[location]]
    print(f"Part 1: {len(pipe_path)//2}")

    enclosed = 0
    for y in range(height):
        within_loop, x = False, -1
        while (x := x + 1) < width:
            if complex(x, y) not in pipe_path:
                enclosed += within_loop
            else:
                pipe_start = grid[complex(x, y)]
                while (pipe_end := grid[complex(x, y)]) not in ("|", "7", "J"):
                    x += 1
                if (
                    (pipe_start == "|")
                    or (pipe_start == "L" and pipe_end == "7")
                    or (pipe_start == "F" and pipe_end == "J")
                ):
                    within_loop = not within_loop
    print(f"Part 2: {enclosed}\n")


solve(example_input)
solve(actual_input)
