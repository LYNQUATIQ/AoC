"""https://adventofcode.com/2023/day/3"""

import os
from functools import cache

with open(os.path.join(os.path.dirname(__file__), "inputs/day03_input.txt")) as f:
    actual_input = f.read()


example_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

Xy = tuple[int, int]

GEAR = "*"


@cache
def number_neighbours(number: str, xy: Xy) -> list[Xy]:
    x, y = xy
    min_x, max_x = x - 1, x + len(number)
    return (
        [(min_x, y), (max_x, y)]
        + [(x, y - 1) for x in range(min_x, max_x + 1)]
        + [(x, y + 1) for x in range(min_x, max_x + 1)]
    )


def solve(inputs: str):
    numbers: dict[Xy, str] = {}
    symbols: dict[Xy, str] = {}

    for y, line in enumerate(inputs.splitlines()):
        current_number = ""
        for x, c in enumerate(line + "."):
            if current_number and not c.isdigit():
                numbers[(x - len(current_number), y)] = current_number
                current_number = ""
            if c == ".":
                continue
            if c.isdigit():
                current_number += c
            else:
                symbols[(x, y)] = c

    total_part_number = 0
    for number_xy, number in numbers.items():
        if any(xy in symbols for xy in number_neighbours(number, number_xy)):
            total_part_number += int(number)
    print(f"Part 1: {total_part_number}")

    total_gear_ratio = 0
    for gear_xy in [xy for xy, symbol in symbols.items() if symbol == GEAR]:
        neighbours = [
            int(number)
            for number_xy, number in numbers.items()
            if any(xy == gear_xy for xy in number_neighbours(number, number_xy))
        ]
        if len(neighbours) == 2:
            total_gear_ratio += neighbours[0] * neighbours[1]
    print(f"Part 2: {total_gear_ratio}\n")


solve(example_input)
solve(actual_input)
