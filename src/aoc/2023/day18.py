"""https://adventofcode.com/2023/day/18"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day18_input.txt")) as f:
    actual_input = f.read()


example_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

DIRECTIONS = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}
HEX_DIRECTIONS = {"0": "R", "1": "D", "2": "L", "3": "U"}
ADJUSTMENTS = {
    # Changing direction on the interior
    ("D", "R", "U"): (-1, 0),
    ("U", "L", "D"): (-1, 0),
    ("L", "D", "R"): (0, -1),
    ("R", "U", "L"): (0, -1),
    # Changing direction on the exterior
    ("U", "R", "D"): (1, 0),
    ("D", "L", "U"): (1, 0),
    ("L", "U", "R"): (0, 1),
    ("R", "D", "L"): (0, 1),
    # Continuing in the same direction
    ("D", "R", "D"): (0, 0),
    ("U", "R", "U"): (0, 0),
    ("D", "L", "D"): (0, 0),
    ("U", "L", "U"): (0, 0),
    ("R", "D", "R"): (0, 0),
    ("L", "D", "L"): (0, 0),
    ("R", "U", "R"): (0, 0),
    ("L", "U", "L"): (0, 0),
}


def shoelace_area(vertices: list[tuple[int, int]]) -> int:
    vertices.append(vertices[0])
    a1, a2 = 0, 0
    for xy1, xy2 in zip(vertices[:-1], vertices[1:]):
        a1 += xy1[0] * xy2[1]
        a2 += xy1[1] * xy2[0]
    return int(abs(a1 - a2) / 2)


def get_vertices(directions: list[str], lengths: list[int]) -> list[tuple[int, int]]:
    vertices, xy = [], (0, 0)
    for i, (direction, length) in enumerate(zip(directions, lengths)):
        prior_direction = directions[i - 1]
        next_direction = directions[(i + 1) % len(directions)]
        ax, ay = ADJUSTMENTS[(prior_direction, direction, next_direction)]
        dx, dy = DIRECTIONS[direction]
        xy = (xy[0] + dx * (length + ax), xy[1] + dy * (length + ay))
        vertices.append(xy)
    assert vertices[-1] == (0, 0)
    return vertices


def get_vertices_part_1(inputs: str):
    directions, lengths = [], []
    for line in inputs.splitlines():
        direction, steps, _ = line.split()
        directions.append(direction)
        lengths.append(int(steps))
    return get_vertices(directions, lengths)


def get_vertices_part_2(inputs: str):
    directions, lengths = [], []
    for line in inputs.splitlines():
        _, _, hexadecimal = line.split()
        directions.append(HEX_DIRECTIONS[hexadecimal[-2:-1]])
        lengths.append(int(hexadecimal[2:-2], 16))
    return get_vertices(directions, lengths)


def solve(inputs: str):
    print(f"Part 1: {shoelace_area(get_vertices_part_1(inputs))}")
    print(f"Part 2: {shoelace_area(get_vertices_part_2(inputs))}\n")


solve(example_input)
solve(actual_input)
