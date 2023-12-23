"""https://adventofcode.com/2023/day/23"""
import os
import re

from collections import defaultdict
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
# #.#v#.##
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
    def __init__(self, grid) -> None:
        self.grid = grid
        self.width, self.height = len(grid[0]), len(grid)
        self.start, self.target = (1, 0), (self.width - 2, self.height - 1)
        self.edges = self.collate_nodes_and_edges()

    def collate_nodes_and_edges(self):
        edges = defaultdict(set)
        to_visit = {(self.start, ((1, 1),))}
        while to_visit:
            this_node, next_nodes = to_visit.pop()
            if this_node == self.target:
                continue
            for next_node in next_nodes:
                last_step, distance = this_node, 0
                while True:
                    distance += 1
                    possible_steps = [
                        s for s in self.possible_steps(next_node) if s != last_step
                    ]
                    if len(possible_steps) != 1:  # Reached another node or a dead end
                        break
                    last_step, next_node = next_node, possible_steps.pop()
                    if next_node == self.target:
                        break
                if not possible_steps:  # Reached a dead end (or a slope we can't climb)
                    if next_node != self.target:  # ...unless we're at the target
                        continue
                if (next_node, distance) not in edges[this_node]:
                    edges[this_node].add((next_node, distance))
                    to_visit.add((next_node, tuple(possible_steps)))

        return edges

    @cache
    def possible_steps(self, here):
        steps = set()
        for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            xy = (here[0] + direction[0], here[1] + direction[1])
            if xy[0] < 0 or xy[1] < 0:
                continue
            next_step = self.grid[xy[1]][xy[0]]
            if next_step == FOREST:
                continue
            if next_step in SLOPES and direction != SLOPE_DIRECTION[next_step]:
                continue
            steps.add(xy)
        return steps

    def find_scenic_path(self):
        to_visit = []
        heappush(to_visit, (0, (self.start, [], 0)))
        while to_visit:
            _, (node, route, total_distance) = heappop(to_visit)
            if node == self.target:
                return total_distance + 1
            for next_node, edge_length in self.edges[node]:
                if next_node in route:
                    continue
                g_score = total_distance + edge_length
                h_score = 0  # (max_time - next_time) * next_flow
                f_score = -g_score + h_score
                heappush(to_visit, (f_score, (next_node, route + [node], g_score)))
        raise RuntimeError("Never got to target")

    def brutal_path(self):
        max_distance = 0
        to_visit = {(self.start, (), 0)}
        while to_visit:
            node, route, total_distance = to_visit.pop()
            if node == self.target:
                max_distance = max(max_distance, total_distance + 1)
                continue
            for next_node, edge_length in self.edges[node]:
                if next_node not in route:
                    new_distance = total_distance + edge_length
                    to_visit.add((next_node, tuple((*route, node)), new_distance))
        return max_distance


@print_time_taken
def solve(inputs: str, answer1, answer2):
    grid = list(inputs.splitlines())
    print(f"Part 1: {Hike(grid).find_scenic_path()}   ({answer1})")

    grid = [re.sub(r">|<|v|\^", ".", line) for line in grid]
    print(f"Part 2: {Hike(grid).find_scenic_path()}   ({answer2})\n")
    # 4714 too low


solve(sample_input, 94, 154)
solve(actual_input, 2370, 6546)
