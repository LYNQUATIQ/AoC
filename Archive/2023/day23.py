"""https://adventofcode.com/2023/day/23"""
import os
import re

from collections import defaultdict

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
        self.edge_lengths = self.collate_edges()

    def next_steps(self, start_xy: tuple[int, int]):
        for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            xy = (start_xy[0] + direction[0], start_xy[1] + direction[1])
            next_step = self.grid.get(xy)
            if next_step != PATH and direction != SLOPE_DIRECTION.get(next_step):
                continue
            yield xy

    def collate_edges(self) -> dict[Node, set[tuple[Node, int]]]:
        edge_lengths = defaultdict(dict)
        to_visit: set[tuple[Node, tuple[Node, ...]]] = {(self.start, ((1, 1),))}
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
                if next_node not in edge_lengths[this_node]:
                    edge_lengths[this_node][next_node] = distance
                    to_visit.add((next_node, tuple(branches)))

        return edge_lengths

    def brutal_path(self) -> int:
        max_distance = 0
        to_visit = {(self.start, (), 0)}
        while to_visit:
            this_node, route, total_distance = to_visit.pop()
            if this_node == self.target:
                max_distance = max(max_distance, total_distance)
                continue
            next_nodes = self.edge_lengths[this_node]
            for next_node, edge_length in next_nodes.items():
                # Don't bother with this branch if one of the other edges goes to target
                if self.target in next_nodes and next_node != self.target:
                    continue
                if next_node not in route:
                    new_distance = total_distance + edge_length
                    to_visit.add((next_node, tuple((*route, this_node)), new_distance))
        return max_distance + 1


@print_time_taken
def solve(inputs: str):
    print(f"\nPart 1: {Hike(inputs).brutal_path()}")

    non_slippery_inputs = re.sub(r">|<|v|\^", ".", inputs)
    print(f"Part2: {Hike(non_slippery_inputs).brutal_path()}\n")


solve(sample_input)
solve(actual_input)
