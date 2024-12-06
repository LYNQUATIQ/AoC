"""https://adventofcode.com/2024/day/6"""

from itertools import product
from os import path

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
LEFT_TURN = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
REVERSE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}


def solve(inputs: str):
    grid = inputs.splitlines()
    width, height = len(grid[0]), len(grid)

    guard_start_xy = None
    obstacles = set()
    for x, y in product(range(width), range(height)):
        if grid[y][x] == "#":
            obstacles.add((x, y))
        elif grid[y][x] == "^":
            guard_start_xy = (x, y)
    assert guard_start_xy is not None

    guard_path = []
    guard_xy = guard_start_xy
    direction = NORTH
    while True:
        assert (guard_xy, direction) not in guard_path
        guard_path.append((guard_xy, direction))
        next_xy = (guard_xy[0] + direction[0], guard_xy[1] + direction[1])
        if not (0 <= next_xy[0] < height and 0 <= next_xy[1] < width):
            break
        if next_xy in obstacles:
            direction = RIGHT_TURN[direction]
            continue
        guard_xy = next_xy

    print(f"Part 1: {len({xy for xy,_ in guard_path})}")

    # Walk the path again, this time keeping track of the places the guard has visited
    obstacle_candidates = set()
    visited = set()
    for guard_xy, direction in guard_path:
        visited.add((guard_xy, direction))
        # print(
        #     guard_xy,
        #     "heading",
        #     {NORTH: "North", SOUTH: "South", EAST: "East", WEST: "West"}[direction],
        # )
        next_xy = (guard_xy[0] + direction[0], guard_xy[1] + direction[1])

        # If we hit an obstacle then reverse back and add the *full* path to visited
        if next_xy in obstacles:
            path_to_here = []
            xy, reverse = guard_xy, REVERSE[direction]
            while (xy, REVERSE[reverse]) not in path_to_here:
                path_to_here.append((xy, REVERSE[reverse]))
                reverse_step = (xy[0] + reverse[0], xy[1] + reverse[1])
                if not (0 <= reverse_step[0] < width and 0 <= reverse_step[1] < height):
                    break
                if reverse_step in obstacles:
                    reverse = LEFT_TURN[reverse]
                    continue
                xy = reverse_step
            visited.update(path_to_here)

        if (guard_xy, RIGHT_TURN[direction]) in visited:
            if 0 <= next_xy[0] < width and 0 <= next_xy[1] < height:
                # print(f"  {next_xy} is a candidate")
                obstacle_candidates.add(next_xy)

    assert guard_start_xy not in obstacle_candidates
    print(f"Part 2: {len(obstacle_candidates)}\n")


solve(example_input)
solve(actual_input)
# 444 too low
