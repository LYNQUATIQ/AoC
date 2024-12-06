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
    obstacles_hit = []
    potential_loop_candidate = None
    loop_candidates = set()
    while True:
        next_step = (guard_xy[0] + direction[0], guard_xy[1] + direction[1])
        if next_step in obstacles:
            obstacles_hit.append(next_step)
            direction = RIGHT_TURN[direction]
            if len(obstacles_hit) >= 3:
                loop_far_corner = obstacles_hit[-3]
                if direction == NORTH:
                    x, y = guard_xy[0], loop_far_corner[1] - 1
                    if y >= 0:
                        potential_loop_candidate = (x, y)
                elif direction == EAST:
                    x, y = loop_far_corner[0] + 1, guard_xy[1]
                    if x < width:
                        potential_loop_candidate = (x, y)
                elif direction == SOUTH:
                    x, y = guard_xy[0], loop_far_corner[1] + 1
                    if y < height:
                        potential_loop_candidate = (x, y)
                elif direction == WEST:
                    x, y = loop_far_corner[0] - 1, guard_xy[1]
                    if x >= 0:
                        potential_loop_candidate = (x, y)
            continue
        if not (0 <= next_step[0] < height and 0 <= next_step[1] < width):
            break

        guard_xy = next_step
        if guard_xy == potential_loop_candidate:
            loop_candidates.add(potential_loop_candidate)
            potential_loop_candidate = None
        guard_xys.add(guard_xy)

    print(f"Part 1: {len(guard_xys)}")
    print(f"Part 2: {len(loop_candidates)}\n")
    print(loop_candidates)


solve(example_input)
# solve(actual_input)
