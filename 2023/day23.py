"""https://adventofcode.com/2023/day/23"""
import os

from functools import cache
from heapq import heappop, heappush

from utils import print_time_taken

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

# sample_input = """#.######
# #.######
# #.#...##
# #.#.#.##
# #.#...##
# #.#.#.##
# #......#
# ######.#"""

ALL_DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SLOPE_DIRECTION = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
SLOPES = set(SLOPE_DIRECTION.keys())
FOREST = "#"

Xy = tuple[int, int]


def manhattan_distance(a, b) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Hike:
    def __init__(self, inputs: str) -> None:
        self.grid = list(inputs.splitlines())
        self.width, self.height = len(self.grid[0]), len(self.grid)
        self.start, self.target = (1, 0), (self.width - 2, self.height - 1)
        self.n_paths = self.width * self.height - sum(
            r.count(FOREST) for r in self.grid
        )

    def is_valid_location(self, xy: Xy) -> bool:
        return (0 <= xy[0] < self.width) and (0 <= xy[1] < self.height)

    def get(self, xy: Xy) -> str:
        return self.grid[xy[1]][xy[0]]

    def trail_map(self, route=None):
        print()
        for y in range(self.height):
            raster = ""
            for x in range(self.width):
                xy = (x, y)
                c = self.get(xy)
                if route is not None and xy in route:
                    c = "o"
                if xy == self.start:
                    c = "S"
                raster += c
            print(raster)
        print()

    @cache
    def possible_moves(self, xy, slippery_slopes_okay):
        moves = []
        for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            next_xy = (xy[0] + direction[0], xy[1] + direction[1])
            if not self.is_valid_location(next_xy):
                continue
            next_step = self.get(next_xy)
            if next_step == FOREST:
                continue
            if not slippery_slopes_okay:
                if next_step in SLOPES and direction != SLOPE_DIRECTION[next_step]:
                    continue
            moves.append(next_xy)
        return moves

    @print_time_taken
    def find_scenic_path(self, slippery_slopes_okay=False):
        to_visit = []
        heappush(to_visit, (0, (self.start, [])))
        while to_visit:
            _, (xy, route) = heappop(to_visit)
            if xy == self.target:
                self.trail_map(route + [self.target])
                return len(route)
            for next_xy in self.possible_moves(xy, slippery_slopes_okay):
                if next_xy not in route:
                    next_route = route + [xy]
                    f_score = len(next_route) - manhattan_distance(xy, next_xy)
                    heappush(to_visit, (f_score, (next_xy, next_route)))
        raise RuntimeError("Never got to target")


def solve(inputs: str):
    hike = Hike(inputs)
    print(f"Part 1: {hike.find_scenic_path()}")

    # print(f"Part 2: {hike.find_scenic_path(slippery_slopes_okay=True)}\n")
    # 4714 too low


solve(sample_input)
# solve(actual_input)
