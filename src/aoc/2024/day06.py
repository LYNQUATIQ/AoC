"""https://adventofcode.com/2024/day/6"""

from itertools import product

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 6)


example_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)
RIGHT_TURN = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}


def solve(inputs: str):
    grid = inputs.splitlines()
    width, height = len(grid[0]), len(grid)

    guard_xy = None
    obstacles = set()
    for x, y in product(range(width), range(height)):
        if grid[y][x] == "#":
            obstacles.add((x, y))
        elif grid[y][x] == "^":
            guard_xy = (x, y)
    assert guard_xy is not None

    guard_xys = {guard_xy}
    direction = NORTH
    obstacles_hit = set()
    while True:
        next_step = (guard_xy[0] + direction[0], guard_xy[1] + direction[1])
        if next_step in obstacles:
            direction = RIGHT_TURN[direction]
            obstacles_hit.add(next_step)
            continue
        if not (0 <= next_step[0] < height and 0 <= next_step[1] < width):
            break
        guard_xy = next_step
        guard_xys.add(guard_xy)

    print(f"Part 1: {len(guard_xys)}")
    print(f"Part 2: {False}\n")


solve(example_input)
# solve(actual_input)
