"""https://adventofcode.com/2023/day/16"""

import os
from collections.abc import Generator
from multiprocessing import Pool
from typing import Iterable

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


NORTH, SOUTH, EAST, WEST = (0, -1), (0, 1), (1, 0), (-1, 0)
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

Grid = list[str]
Beam = tuple[tuple[int, int], tuple[int, int]]  # Location and direction


def process_beam(state: tuple[Beam, Grid]) -> int:
    initial_beam, grid = state
    width, height = len(grid[0]), len(grid)
    energised_tiles, visited = set(), set()
    beams = {initial_beam}
    while beams:
        new_beams = set()
        for location, direction in beams:
            new_location = (location[0] + direction[0], location[1] + direction[1])
            x, y = new_location
            if not (0 <= x < width and 0 <= y < height):
                continue
            energised_tiles.add(new_location)
            for new_direction in DIRECTIONS[(direction, grid[y][x])]:
                new_beam = (new_location, new_direction)
                if new_beam in visited:
                    continue
                visited.add(new_beam)
                new_beams.add(new_beam)
        beams = new_beams
    return len(energised_tiles)


def initial_beams(grid: Grid) -> Generator[Iterable[tuple[Beam, Grid]]]:
    width, height = len(grid[0]), len(grid)
    for x in range(width):
        yield ((((x, -1), SOUTH), grid))
        yield ((((x, height), NORTH), grid))
    for y in range(height):
        yield ((((-1, y), EAST), grid))
        yield ((((width, y), WEST), grid))


def solve(inputs: str):
    grid = inputs.splitlines()
    print(f"Part 1: {process_beam((((-1,0), EAST), grid))}")

    with Pool(processes=4) as pool:
        energy_values = list(pool.imap_unordered(process_beam, initial_beams(grid)))
    print(f"Part 2: {max(energy_values)}\n")


if __name__ == "__main__":
    solve(sample_input)
    solve(actual_input)
