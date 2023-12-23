"""https://adventofcode.com/2023/day/23"""
import os
import re

from collections import defaultdict
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


SLOPE_DIRECTION = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
FOREST, PATH = "#", "."

Node = tuple[int, int]


class Hike:
    def __init__(self, inputs: str) -> None:
        self.grid = {}
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                self.grid[(x, y)] = c
        self.start, self.target = (1, 0), (x - 1, y)
        self.grid[self.start] = FOREST
        self.edges = self.collate_nodes_and_edges()

    def next_steps(self, start_xy: tuple[int, int]):
        for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            xy = (start_xy[0] + direction[0], start_xy[1] + direction[1])
            next_step = self.grid.get(xy)
            if next_step != PATH and direction != SLOPE_DIRECTION.get(next_step):
                continue
            yield xy

    def collate_nodes_and_edges(self) -> dict[Node, set[tuple[Node, int]]]:
        edges = defaultdict(set)
        to_visit: set[tuple[Node, tuple[Node, ...]]] = {(self.start, ((1, 2),))}
        while to_visit:
            this_node, next_nodes = to_visit.pop()
            if this_node == self.target:
                continue
            for next_node in next_nodes:
                last_step, distance = this_node, 0
                while True:
                    distance += 1
                    branches = [s for s in self.next_steps(next_node) if s != last_step]
                    if len(branches) != 1:  # Reached another node or a dead end
                        break
                    last_step, next_node = next_node, branches.pop()
                    if next_node == self.target:
                        break
                if not branches:  # Reached a dead end (or a slope we can't climb)
                    if next_node != self.target:  # ...unless we're at the target
                        continue
                if (next_node, distance) not in edges[this_node]:
                    edges[this_node].add((next_node, distance))
                    to_visit.add((next_node, tuple(branches)))

        return edges

    def scenic_path(self) -> int:
        to_visit = [(0, (self.start, [], 0))]
        while to_visit:
            _, (node, route, total_distance) = heappop(to_visit)
            if node == self.target:
                return total_distance
            for next_node, edge_length in self.edges[node]:
                if next_node in route:
                    continue
                g_score = total_distance + edge_length
                h_score = sum(d for n, d in self.edges[node])  # if n != node)
                f_score = -g_score - h_score
                heappush(to_visit, (f_score, (next_node, route + [node], g_score)))
        raise RuntimeError("Never got to target")

    def brutal_path(self) -> int:
        max_distance = 0
        to_visit = {(self.start, (), 0)}
        while to_visit:
            node, route, total_distance = to_visit.pop()
            if node == self.target:
                max_distance = max(max_distance, total_distance)
                continue
            for next_node, edge_length in self.edges[node]:
                if next_node not in route:
                    new_distance = total_distance + edge_length
                    to_visit.add((next_node, tuple((*route, node)), new_distance))
        return max_distance


@print_time_taken
def solve(inputs: str):
    print(f"Part 1: {Hike(inputs).brutal_path()}   (Brute Force)")
    print(f"Part 1: {Hike(inputs).scenic_path()}\n")

    non_slippery_inputs = re.sub(r">|<|v|\^", ".", inputs)
    print(f"Part 2: {Hike(non_slippery_inputs).brutal_path()}   (Brute Force)")
    print(f"Part 2: {Hike(non_slippery_inputs).scenic_path()}\n")


solve(sample_input)
# solve(actual_input)
