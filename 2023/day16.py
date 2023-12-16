"""https://adventofcode.com/2023/day/16"""
import os
from multiprocessing import Pool

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
    (NORTH, "\\"): (WEST,),
    (SOUTH, "\\"): (EAST,),
    (EAST, "\\"): (SOUTH,),
    (WEST, "\\"): (NORTH,),
    (NORTH, "."): (NORTH,),
    (SOUTH, "."): (SOUTH,),
    (EAST, "."): (EAST,),
    (WEST, "."): (WEST,),
}

Location = complex
Direction = complex
Beam = tuple[Location, Direction]


def process_beam(start_beam, grid):
    energised_tiles, visited = set(), set()
    beams = {start_beam}
    while beams:
        new_beams = set()
        for location, direction in beams:
            new_location = location + direction
            if new_location not in grid:
                continue
            energised_tiles.add(new_location)
            for new_direction in DIRECTIONS[(direction, grid[new_location])]:
                new_beam = (new_location, new_direction)
                if new_beam in visited:
                    continue
                visited.add(new_beam)
                new_beams.add(new_beam)
        beams = new_beams
    return len(energised_tiles)


def solve(inputs: str):
    grid: dict[Location, str] = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            grid[complex(x, y)] = c
    width, height = x + 1, y + 1

    print(f"Part 1: {process_beam((-1, EAST), grid)}")

    south_beams = {(complex(x, -1), SOUTH) for x in range(width)}
    north_beams = {(complex(x, height), NORTH) for x in range(width)}
    east_beams = {(complex(-1, y), EAST) for y in range(height)}
    west_beams = {(complex(width, y), EAST) for y in range(height)}
    start_beams = south_beams | north_beams | east_beams | west_beams

    energy_values = Pool(processes=4).starmap(
        process_beam, [(start_beam, grid) for start_beam in start_beams]
    )
    print(f"Part 2: {max(energy_values)}\n")


if __name__ == "__main__":
    solve(sample_input)
    solve(actual_input)
