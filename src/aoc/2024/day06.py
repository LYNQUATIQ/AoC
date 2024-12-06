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
LEFT_TURN = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}


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

    # Keep track of the places the guard has visited
    guard_path = []
    direction = NORTH
    while True:
        assert (guard_xy, direction) not in guard_path
        guard_path.append((guard_xy, direction))
        next_xy = (guard_xy[0] + direction[0], guard_xy[1] + direction[1])
        if next_xy in obstacles:
            direction = RIGHT_TURN[direction]
            continue
        if not (0 <= next_xy[0] < height and 0 <= next_xy[1] < width):
            break
        guard_xy = next_xy

    print(f"Part 1: {len({xy for xy,_ in guard_path})}")

    # Track the places the guard visited (including the path to the start)
    visited = set()
    xy, _ = guard_path[0]
    direction, reverse = NORTH, SOUTH
    while True:
        assert (xy, direction) not in visited
        visited.add((xy, direction))
        reverse_step = (xy[0] + reverse[0], xy[1] + reverse[1])
        if reverse_step in obstacles:
            direction = LEFT_TURN[reverse]
            continue
        if not (0 <= reverse_step[0] < height and 0 <= reverse_step[1] < width):
            break
        xy = reverse_step

    obstacle_candidates = set()
    for guard_xy, direction in guard_path:
        print(
            guard_xy,
            "heading",
            {NORTH: "North", SOUTH: "South", EAST: "East", WEST: "West"}[direction],
        )
        next_xy = (guard_xy[0] + direction[0], guard_xy[1] + direction[1])
        if next_xy in obstacles:
            continue
        if (xy, RIGHT_TURN[direction]) in visited:
            obstacle_xy = (xy[0] + direction[0], xy[1] + direction[1])
            if 0 <= obstacle_xy[0] < height and 0 <= obstacle_xy[1] < width:
                print(f"  {obstacle_xy} is a candidate")
                obstacle_candidates.add(obstacle_xy)
        visited.add((guard_xy, direction))

    print(f"Part 2: {len(obstacle_candidates)}\n")

    print(sorted([(3, 6), (6, 7), (7, 7), (1, 8), (3, 8), (7, 9)]))


solve(example_input)
# solve(actual_input)
