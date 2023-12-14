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

BOULDER, ROCK, SPACE = "O", "#", "."


@cache
def tilt(rows: tuple[str]) -> tuple[str]:
    grid = [list(row) for row in rows]
    width, height = len(grid[0]), len(grid)
    for x in range(width):
        y, last_space = 0, None
        while y < height:
            while y < height and grid[y][x] != SPACE:
                y += 1
            while y < height and grid[y][x] == SPACE:
                last_space = y if last_space is None else last_space
                y += 1
            if y < height and grid[y][x] == BOULDER and last_space is not None:
                grid[last_space][x], grid[y][x] = BOULDER, SPACE
                last_space += 1
            else:
                last_space = None
    return tuple("".join(row) for row in grid)


@cache
def cycle(rows: tuple[str]) -> tuple[str]:
    for _ in range(4):
        rows = tilt(rows)
        rows = tuple("".join(column[::-1]) for column in zip(*rows))  # Rotate clockwise
    return rows


def calculate_load(rows: tuple[str]) -> int:
    return sum(rank * row.count(BOULDER) for rank, row in enumerate(rows[::-1], 1))


def solve(inputs: str):
    rows = tuple(inputs.splitlines())

    print(f"Part 1: {calculate_load(tilt(rows))}")

    i, visited, states = 0, {}, [rows]
    while i <= 1_000_000_000:
        i += 1
        states.append(rows := cycle(rows))
        if prior_i := visited.get(rows):
            rows = states[(1_000_000_000 - prior_i) % (i - prior_i) + prior_i]
            break
        visited[rows] = i
    print(f"Part 2: {calculate_load(rows)}\n")


solve(sample_input)
solve(actual_input)
