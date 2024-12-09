"""https://adventofcode.com/2024/day/6"""

from collections import defaultdict

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
    height, width = y + 1, x + 1

    # Walk the guard path for part 1 and remember the positions visited
    guard_positions = []
    xy, heading = start_xy, NORTH
    while True:
        next_xy = xy + heading
        if not (0 <= xy.real < width and 0 <= xy.imag < height):
            break
        guard_positions.append((xy, heading))
        if next_xy in obstacles:
            heading = RIGHT_TURN[heading]
            continue
        xy = next_xy

    print(f"Part 1: {len({p for p,_ in guard_positions})}")

    # Precompute all the edges that lead away from the obstacles
    def get_edge_end(origin_xy, heading):
        """Given a starting point/heading work out endpoint (i.e. obstacle or off map)"""
        xy = origin_xy
        while True:
            next_xy = xy + heading
            if next_xy in obstacles:
                return xy
            if not (0 <= xy.real < width and 0 <= xy.imag < height):
                return OFF_MAP
            xy = next_xy

    edges = defaultdict(dict)
    edges[NORTH][start_xy] = get_edge_end(start_xy, NORTH)
    for obstacle in obstacles:
        for neighbour_direction in (NORTH, SOUTH, EAST, WEST):
            neighour_xy = obstacle + neighbour_direction
            heading = REVERSE[neighbour_direction]
            heading = RIGHT_TURN[heading]
            edges[heading][neighour_xy] = get_edge_end(neighour_xy, heading)

    # Loop over the steps in the path and test adding an extra obstacle ahead of us
    obstacle_candidates = set()
    for path_xy, path_heading in guard_positions:
        extra_obstacle = path_xy + path_heading
        if extra_obstacle in obstacles or extra_obstacle == start_xy:
            continue
        # Find edges that need to be overridden, and add extra ones due to new obstacle
        obstacle_x, obstacle_y = extra_obstacle.real, extra_obstacle.imag
        extra_edges = defaultdict(dict)
        for edge_direction in (NORTH, SOUTH, EAST, WEST):
            for start, end in edges[edge_direction].items():
                x0, y0 = start.real, start.imag
                x1, y1 = end.real, end.imag
                if edge_direction == NORTH:
                    if (obstacle_x != x0) or not (y0 > obstacle_y >= y1):
                        continue
                    xy, heading_out = extra_obstacle + SOUTH, RIGHT_TURN[edge_direction]
                elif edge_direction == SOUTH:
                    y1 = height if y1 == -1 else y1
                    if (obstacle_x != x0) or not (y0 < obstacle_y <= y1):
                        continue
                    xy, heading_out = extra_obstacle + NORTH, RIGHT_TURN[edge_direction]
                elif edge_direction == EAST:
                    x1 = width if x1 == -1 else x1
                    if (obstacle_y != y0) or not (x0 < obstacle_x <= x1):
                        continue
                    xy, heading_out = extra_obstacle + WEST, RIGHT_TURN[edge_direction]
                elif edge_direction == WEST:
                    if (obstacle_y != y0) or not (x0 > obstacle_x >= x1):
                        continue
                    xy, heading_out = extra_obstacle + EAST, RIGHT_TURN[edge_direction]
                # Found edge hitting the extra obstacle; shorten it and add new one
                extra_edges[edge_direction][start] = xy
                extra_edges[heading_out][xy] = get_edge_end(xy, heading_out)

        # Test if the extra obstacle (i.e. extra edges) causes a loop
        xy, heading, visited = start_xy, NORTH, set()
        while xy != OFF_MAP:
            if (xy, heading) in visited:
                obstacle_candidates.add(extra_obstacle)  # Found a loop
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
