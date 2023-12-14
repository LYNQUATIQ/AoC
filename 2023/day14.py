"""https://adventofcode.com/2023/day/14"""
import os

from functools import cache

with open(os.path.join(os.path.dirname(__file__), "inputs/day14_input.txt")) as f:
    actual_input = f.read()


sample_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

BOULDER, SPACE = "O", "."


@cache
def tilt(rows: tuple[str]) -> tuple[str]:
    rows = list(rows)
    something_rolled = True
    while something_rolled:
        something_rolled = False
        prior_row = rows[0]
        for y, this_row in enumerate(rows[1:], 1):
            new_prior_row, new_this_row = "", ""
            for this_c, prior_c in zip(this_row, prior_row):
                roll_it = this_c == BOULDER and prior_c == SPACE
                new_prior_row += BOULDER if roll_it else prior_c
                new_this_row += SPACE if roll_it else this_c
                something_rolled |= roll_it
            rows[y - 1], rows[y] = new_prior_row, new_this_row
            prior_row = new_this_row
    return tuple(rows)


@cache
def cycle(rows: tuple[str]) -> tuple[str]:
    for _ in range(4):
        rows = tilt(rows)
        rows = tuple("".join(row[::-1]) for row in zip(*rows))  # Rotate clockwise
    return rows


def calculate_load(rows: tuple[str]) -> int:
    return sum(rank * row.count(BOULDER) for rank, row in enumerate(rows[::-1], 1))


def solve(inputs: str):
    rows = tuple(inputs.splitlines())
    print(f"Part 1: {calculate_load(tilt(rows))}")

    rows = tuple(inputs.splitlines())
    i, visited, states = 0, {}, [rows]
    while i <= 1_000_000_000:
        i += 1
        rows = cycle(rows)
        states.append((rows))
        if (prior_i := visited.get(rows)) is not None:
            rows = states[(1_000_000_000 - prior_i) % (i - prior_i) + prior_i]
            break
        visited[rows] = i
    print(f"Part 2: {calculate_load(rows)}\n")


solve(sample_input)
solve(actual_input)
