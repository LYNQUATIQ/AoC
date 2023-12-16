"""https://adventofcode.com/2023/day/16"""
import os
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day16_input.txt")) as f:
    actual_input = f.read()


sample_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


NORTH, SOUTH, EAST, WEST = -1j, +1j, 1, -1
DIRECTIONS = {
    (NORTH, "|"): (NORTH,),
    (SOUTH, "|"): (SOUTH,),
    (EAST, "|"): (NORTH, SOUTH),
    (WEST, "|"): (NORTH, SOUTH),
    (NORTH, "-"): (EAST, WEST),
    (SOUTH, "-"): (EAST, WEST),
    (EAST, "-"): (EAST,),
    (WEST, "-"): (WEST,),
    (NORTH, "/"): (EAST,),
    (SOUTH, "/"): (WEST,),
    (EAST, "/"): (NORTH,),
    (WEST, "/"): (SOUTH,),
    (NORTH, chr(92)): (WEST,),
    (SOUTH, chr(92)): (EAST,),
    (EAST, chr(92)): (SOUTH,),
    (WEST, chr(92)): (NORTH,),
    (NORTH, "."): (NORTH,),
    (SOUTH, "."): (SOUTH,),
    (EAST, "."): (EAST,),
    (WEST, "."): (WEST,),
}


def solve(inputs: str):
    grid = inputs.splitlines()
    width, height = len(grid[0]), len(grid)

    start_beams = set()
    for x in range(width):
        start_beams.add((complex(x, -1), SOUTH))
        start_beams.add((complex(x, height), NORTH))
    for y in range(height):
        start_beams.add((complex(-1, y), EAST))
        start_beams.add((complex(width, y), WEST))

    energised = defaultdict(set)
    for start_beam in start_beams:
        beams = {start_beam}
        visited = set()
        while beams:
            new_beams = set()
            for location, direction in beams:
                location += direction
                x, y = int(location.real), int(location.imag)
                if not (0 <= x < width and 0 <= y < height):
                    continue
                reflector = grid[y][x]
                energised[start_beam].add(location)
                for new_direction in DIRECTIONS[(direction, reflector)]:
                    if (location, new_direction) in visited:
                        continue
                    visited.add((location, new_direction))
                    new_beams.add((location, new_direction))
            beams = new_beams

    energised = {k: len(v) for k, v in energised.items()}
    print(f"Part 1: {energised[(-1, EAST)]}")
    print(f"Part 2: {max(energised.values())}\n")


solve(sample_input)
solve(actual_input)
