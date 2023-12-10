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
    width, height = x + 1, y + 1

    valid_headings = tuple(
        heading
        for heading in (NORTH, SOUTH, EAST, WEST)
        if (heading, grid.get(start + heading)) in DIRECTIONS
    )
    grid[start] = {
        (NORTH, SOUTH): "|",
        (NORTH, EAST): "L",
        (NORTH, WEST): "J",
        (SOUTH, EAST): "F",
        (SOUTH, WEST): "7",
        (EAST, WEST): "-",
    }[valid_headings]

    direction = valid_headings[0]
    path, location = {start}, start + direction
    while location != start:
        path.add(location)
        direction = DIRECTIONS[direction, grid[location]]
        location += direction
    print(f"Part 1: {len(path)//2}")

    enclosed = 0
    for y in range(height):
        within_loop, x = False, 0
        while x < width:
            if within_loop and complex(x, y) not in path:
                enclosed += 1
            while x < width and complex(x, y) not in path:
                x += 1
                if within_loop and complex(x, y) not in path:
                    enclosed += 1
            if x >= width:
                break
            pipe = grid[complex(x, y)]
            if pipe == "|":
                within_loop = not within_loop
            elif pipe == "L":
                x += 1
                while grid[complex(x, y)] == "-":
                    x += 1
                if grid[complex(x, y)] == "7":
                    within_loop = not within_loop
            elif pipe == "F":
                x += 1
                while grid[complex(x, y)] == "-":
                    x += 1
                if grid[complex(x, y)] == "J":
                    within_loop = not within_loop
            x += 1

    print(f"Part 2: {enclosed}\n")


solve(sample_input)
solve(actual_input)
