"""https://adventofcode.com/2024/day/6"""

import multiprocessing

from functools import partial

from aoc_utils import get_input_data, print_time_taken

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

NORTH = -1j
SOUTH = +1j
EAST = +1
WEST = -1
RIGHT_TURN = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}


def test_obstacle_for_loop(extra_obstacle, start_xy, obstacles, width, height):
    path_out = set()
    xy, heading = start_xy, NORTH
    while True:
        if (xy, heading) in path_out:
            return extra_obstacle
        next_xy = xy + heading
        if not (0 <= xy.real < width and 0 <= xy.imag < height):
            return start_xy
        path_out.add((xy, heading))
        if (next_xy in obstacles) or (next_xy == extra_obstacle):
            heading = RIGHT_TURN[heading]
            continue
        xy = next_xy


@print_time_taken
def solve(inputs: str):

    start_xy = None
    obstacles = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            xy = complex(x, y)
            if c == "#":
                obstacles.add(xy)
            elif c == "^":
                start_xy = xy
    height, width = y + 1, x + 1

    guard_path = []
    xy, heading = start_xy, NORTH
    while True:
        next_xy = xy + heading
        if not (0 <= xy.real < width and 0 <= xy.imag < height):
            break
        if next_xy in obstacles:
            heading = RIGHT_TURN[heading]
            continue
        guard_path.append((xy, heading))
        xy = next_xy

    print(f"Part 1: {len({p for p,_ in guard_path})}")

    obstacle_candidates = {xy + heading for xy, heading in guard_path}
    obstacle_candidates = obstacle_candidates - obstacles
    test_obstacle_task = partial(
        test_obstacle_for_loop,
        start_xy=start_xy,
        obstacles=obstacles,
        width=width,
        height=height,
    )
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(test_obstacle_task, obstacle_candidates)

    obstacle_sites = set(results)
    obstacle_sites.discard(start_xy)
    print(f"Part 2: {len(obstacle_sites)}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
