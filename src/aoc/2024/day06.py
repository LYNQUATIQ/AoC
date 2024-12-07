"""https://adventofcode.com/2024/day/6"""

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

    def path_out(extra_obstacle=None):
        path_out = set()
        xy, heading = start_xy, NORTH
        while True:
            if (xy, heading) in path_out:
                return None
            next_xy = xy + heading
            if not (0 <= xy.real < width and 0 <= xy.imag < height):
                return path_out
            path_out.add((xy, heading))
            if (next_xy in obstacles) or (next_xy == extra_obstacle):
                heading = RIGHT_TURN[heading]
                continue
            xy = next_xy

    guard_path = path_out()
    print(f"Part 1: {len({p for p,_ in guard_path})}")

    obstacle_candidates = set()
    for xy, heading in guard_path:
        # If we were to add a hypothetical obstacle ahead of us would we still leave?
        new_obstacle = xy + heading
        if new_obstacle in obstacles or new_obstacle == start_xy:
            continue
        if path_out(new_obstacle) is None:
            obstacle_candidates.add(new_obstacle)

    print(f"Part 2: {len(obstacle_candidates)}\n")


solve(example_input)
solve(actual_input)
