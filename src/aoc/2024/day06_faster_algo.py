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

    def get_edge_end(origin_xy, heading):
        xy = origin_xy
        while True:
            next_xy = xy + heading
            if next_xy in obstacles:
                return xy
            if not (0 <= xy.real < width and 0 <= xy.imag < height):
                return OFF_MAP
            xy = next_xy

    # Precompute all the edges that lead away from the obstacles
    edges = defaultdict(dict)
    edges[NORTH][start_xy] = get_edge_end(start_xy, NORTH)
    for obstacle in obstacles:
        for neighbour_direction in (NORTH, SOUTH, EAST, WEST):
            neighour_xy = obstacle + neighbour_direction
            heading = REVERSE[neighbour_direction]
            heading = RIGHT_TURN[heading]
            edges[heading][neighour_xy] = get_edge_end(neighour_xy, heading)

    # Walk the guard path for part 1 and remember the positions visited
    guard_positions = set()
    xy, heading = start_xy, NORTH
    while True:
        next_xy = xy + heading
        if not (0 <= xy.real < width and 0 <= xy.imag < height):
            break
        guard_positions.add((xy, heading))
        if next_xy in obstacles:
            heading = RIGHT_TURN[heading]
            continue
        xy = next_xy

    print(f"Part 1: {len({p for p,_ in guard_positions})}")

    def is_loop(overrides):
        xy, heading = start_xy, NORTH
        visited = set()
        while True:
            if (xy, heading) in visited:
                return True
            visited.add((xy, heading))
            try:
                next_xy = overrides[heading][xy]
            except KeyError:
                next_xy = edges[heading][xy]
            if next_xy is OFF_MAP:
                return False
            xy, heading = next_xy, RIGHT_TURN[heading]

    obstacle_candidates = set()
    for path_xy, path_heading in guard_positions:

        # If we were to add a hypothetical obstacle ahead of us would we create a loop?
        new_obstacle = path_xy + path_heading
        if new_obstacle in obstacles or new_obstacle == start_xy:
            continue

        # Find edges that need to be overridden, and add new ones from new obstacle...
        obstacle_x, obstacle_y = new_obstacle.real, new_obstacle.imag
        overrides = defaultdict(dict)
        for heading in (NORTH, SOUTH, EAST, WEST):
            for start, end in edges[heading].items():
                start_x, start_y = start.real, start.imag
                if end is OFF_MAP:
                    end_x, end_y = {
                        NORTH: (start_x, -1),
                        SOUTH: (start_x, height),
                        EAST: (width, start_y),
                        WEST: (-1, start_y),
                    }[heading]
                else:
                    end_x, end_y = end.real, end.imag
                if heading in (NORTH, SOUTH):
                    if obstacle_x != start_x:
                        continue
                    if heading == NORTH:
                        if not (start_y > obstacle_y >= end_y):
                            continue
                        xy, heading_out = new_obstacle + SOUTH, RIGHT_TURN[heading]
                        overrides[heading][start] = xy
                        overrides[heading_out][xy] = get_edge_end(xy, heading_out)

                    elif heading == SOUTH:
                        if not (start_y < obstacle_y <= end_y):
                            continue
                        xy, heading_out = new_obstacle + NORTH, RIGHT_TURN[heading]
                        overrides[heading][start] = xy
                        overrides[heading_out][xy] = get_edge_end(xy, heading_out)
                elif heading in (EAST, WEST):
                    if obstacle_y != start_y:
                        continue
                    if heading == EAST:
                        if not (start_x < obstacle_x <= end_x):
                            continue
                        xy, heading_out = new_obstacle + WEST, RIGHT_TURN[heading]
                        overrides[heading][start] = xy
                        overrides[heading_out][xy] = get_edge_end(xy, heading_out)
                    elif heading == WEST:
                        if not (start_x > obstacle_x >= end_x):
                            continue
                        xy, heading_out = new_obstacle + EAST, RIGHT_TURN[heading]
                        overrides[heading][start] = xy
                        overrides[heading_out][xy] = get_edge_end(xy, heading_out)

        if is_loop(overrides):
            obstacle_candidates.add(new_obstacle)

    print(f"Part 2: {len(obstacle_candidates)}\n")


solve(example_input)
solve(actual_input)
