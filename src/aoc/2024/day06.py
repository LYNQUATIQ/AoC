"""https://adventofcode.com/2024/day/6"""

from functools import cache

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

    start_xy = None
    obstacles = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            if c == "#":
                obstacles.add((x, y))
            elif c == "^":
                start_xy = (x, y)
    height, width = y + 1, x + 1

    @cache
    def path_from_here(xy, heading, extra_obstacle=None):
        path_from_here = set()
        while True:
            if (xy, heading) in path_from_here:
                return None
            next_xy = (xy[0] + heading[0], xy[1] + heading[1])
            if not (0 <= xy[0] < width and 0 <= xy[1] < height):
                return path_from_here
            path_from_here.add((xy, heading))
            if (next_xy in obstacles) or (next_xy == extra_obstacle):
                heading = RIGHT_TURN[heading]
                continue
            xy = next_xy

    guard_path = path_from_here(start_xy, NORTH)
    print(f"Part 1: {len({p for p,_ in guard_path})}")

    obstacle_candidates = set()
    for xy, heading in guard_path:
        # If we were to add a hypothetical obstacle ahead of us would we still leave?
        obstacle = (xy[0] + heading[0], xy[1] + heading[1])
        if obstacle in obstacles or obstacle == start_xy:
            continue
        if path_from_here(start_xy, NORTH, obstacle) is None:
            # print("  Found obstacle candidate", obstacle)
            obstacle_candidates.add(obstacle)

    print(f"Part 2: {len(obstacle_candidates)}\n")

    # print("Obstacle candidates:", sorted(obstacle_candidates))


solve(example_input)
solve(actual_input)
# 853 too low, 1253 wrong, 1819 wrong
