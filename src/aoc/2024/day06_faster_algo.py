"""https://adventofcode.com/2024/day/6"""

from collections import defaultdict
from itertools import product

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
LEFT_TURN = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
REVERSE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
OFF_MAP = complex(-1, -1)


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
    max_y, max_w = y + 1, x + 1

    # Walk the steps the guard takes for part 1 and remember the positions visited
    guard_positions = []
    xy, heading = start_xy, NORTH
    while True:
        next_xy = xy + heading
        if not (0 <= xy.real < max_w and 0 <= xy.imag < max_y):
            break
        guard_positions.append((xy, heading))
        if next_xy in obstacles:
            heading = RIGHT_TURN[heading]
            continue
        xy = next_xy

    print(f"Part 1: {len({p for p,_ in guard_positions})}")

    # For part 2... precompute all the edges that lead away from the obstacles
    def get_edge_end(origin_xy, heading):
        """Given an origin point/heading work out end point (i.e. obstacle or off map)"""
        xy = origin_xy
        while True:
            next_xy = xy + heading
            if next_xy in obstacles:
                return xy
            if not (0 <= xy.real < max_w and 0 <= xy.imag < max_y):
                return OFF_MAP
            xy = next_xy

    edges = defaultdict(dict)
    for obstacle, neighbour_direction in product(obstacles, (NORTH, SOUTH, EAST, WEST)):
        turn_xy = obstacle + neighbour_direction
        new_heading = LEFT_TURN[neighbour_direction]
        edges[new_heading][turn_xy] = get_edge_end(turn_xy, new_heading)
    edges[NORTH][start_xy] = get_edge_end(start_xy, NORTH)  # Add the initial 'edge'

    # Loop over the steps in the path and test adding an extra obstacle ahead of us
    obstacle_candidates = set()
    for path_xy, path_heading in guard_positions:
        extra_obstacle = path_xy + path_heading
        if extra_obstacle in obstacles or extra_obstacle == start_xy:
            continue
        # Find edges that should be shortened due to new obstacle and add extra 'turn'
        extra_x, extra_y = extra_obstacle.real, extra_obstacle.imag
        extra_edges = defaultdict(dict)
        for edge_heading, directional_edges in edges.items():
            for edge_start, edge_end in directional_edges.items():
                x0, y0 = edge_start.real, edge_start.imag
                x1, y1 = edge_end.real, edge_end.imag
                if edge_heading == NORTH:
                    if extra_x != x0 or not y0 > extra_y >= y1:
                        continue
                elif edge_heading == SOUTH:
                    if extra_x != x0 or not y0 < extra_y <= (max_y if y1 == -1 else y1):
                        continue
                elif edge_heading == EAST:
                    if extra_y != y0 or not x0 < extra_x <= (max_w if x1 == -1 else x1):
                        continue
                elif edge_heading == WEST:
                    if extra_y != y0 or not x0 > extra_x >= x1:
                        continue
                # Found edge hitting the extra obstacle; shorten it and add new edge
                turn_xy = extra_obstacle + REVERSE[edge_heading]
                new_heading = RIGHT_TURN[edge_heading]
                extra_edges[edge_heading][edge_start] = turn_xy
                extra_edges[new_heading][turn_xy] = get_edge_end(turn_xy, new_heading)

        # Test if the extra obstacle (extra edges) now causes a loop
        xy, heading, visited = start_xy, NORTH, set()
        while xy != OFF_MAP:
            if (xy, heading) in visited:  # Found a loop
                obstacle_candidates.add(extra_obstacle)
                break
            visited.add((xy, heading))
            try:
                xy = extra_edges[heading][xy]
            except KeyError:
                xy = edges[heading][xy]
            heading = RIGHT_TURN[heading]

    print(f"Part 2: {len(obstacle_candidates)}\n")


solve(example_input)
solve(actual_input)
