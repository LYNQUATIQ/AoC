"""https://adventofcode.com/2023/day/23"""
import os

from functools import cache
from heapq import heappop, heappush

with open(os.path.join(os.path.dirname(__file__), "inputs/day23_input.txt")) as f:
    actual_input = f.read()


sample_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

# sample_input = """#.####
# #.>..#
# ####.#"""

ALL_DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SLOPE_DIRECTION = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
SLOPES = set(SLOPE_DIRECTION.keys())
FOREST = "#"
PATH = "."


@cache
def possible_moves(xy, grid, slippery_slopes_okay):
    moves = []
    for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        x1, y1 = xy[0] + direction[0], xy[1] + direction[1]
        if x1 < 0 or y1 < 0:
            continue
        next_step = grid[y1][x1]
        if next_step == FOREST:
            continue
        if not slippery_slopes_okay:
            if next_step in SLOPES and direction != SLOPE_DIRECTION[next_step]:
                continue
        moves.append((x1, y1))
    return moves


from utils import print_time_taken


@print_time_taken
def find_scenic_path(grid, slippery_slopes_okay=False):
    start, target = (1, 0), (len(grid[0]) - 2, len(grid) - 1)
    routes_to_target = {}
    to_visit = {(start, ())}
    while to_visit:
        xy, route = to_visit.pop()
        if xy == target:
            routes_to_target[len(route)] = route
            continue
        for next_xy in possible_moves(xy, grid, slippery_slopes_okay):
            if next_xy not in route:
                to_visit.add((next_xy, tuple((*route, xy))))
    return max(routes_to_target)


def solve(inputs: str):
    grid = tuple(inputs.splitlines())
    print(f"Part 1: {find_scenic_path(grid)}")
    print(f"Part 2: {find_scenic_path(grid, slippery_slopes_okay=True)}\n")


solve(sample_input)
solve(actual_input)
