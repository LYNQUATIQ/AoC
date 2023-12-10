"""https://adventofcode.com/2023/day/10"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()


sample_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

# sample_input = """.F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ..."""

# sample_input = """FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L"""

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

    enclosed = set()
    for y in range(height):
        within_loop, x = False, 0
        while x < width:
            if within_loop and complex(x, y) not in path:
                enclosed.add(complex(x, y))
            while x < width and complex(x, y) not in path:
                x += 1
                if within_loop and complex(x, y) not in path:
                    enclosed.add(complex(x, y))
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

    # for y in range(height):
    #     line = ""
    #     for x in range(width):
    #         line += "\u2589" if complex(x, y) in enclosed else grid[complex(x, y)]
    #     print(line)

    print(f"Part 2: {len(enclosed)}\n")


solve(sample_input)
solve(actual_input)
# 441 is too high
