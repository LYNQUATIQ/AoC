"""https://adventofcode.com/2022/day/12"""
import os

from typing import Iterable

from grid import Grid, XY
from search import a_star
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class HillGrid(Grid):
    def __init__(self, inputs: str) -> None:
        self._grid = {}
        self.start, self.target = XY(0, 0), XY(0, 0)
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                xy = XY(x, y)
                if c == "S":
                    c = "a"
                    self.start = xy
                elif c == "E":
                    c = "z"
                    self.target = xy
                self._grid[xy] = c
        self._limits = self.limits

    def connected_nodes(
        self, node: XY, blockages: Iterable[XY] | None = None
    ) -> list[XY]:
        return [
            n
            for n in node.neighbours
            if n.in_bounds(self._limits) and (ord(self[n]) - ord(self[node])) <= 1
        ]

    def lowest_nodes(self) -> list[XY]:
        return [n for n in self._grid if self[n] == "a"]

    def heuristic(self, node: XY, next_node: XY) -> int:
        h_distance = (node - next_node).manhattan_distance
        v_distance = ord(self[next_node]) - ord(self[node])
        return v_distance + h_distance

    def shortest_path(self, start: XY | None = None) -> list[XY] | None:
        start = self.start if start is None else start
        path = a_star(self, start, self.target)
        return path


@print_time_taken
def solve(inputs: str) -> None:
    hill = HillGrid(inputs)

    print(f"Part 1: {len(hill.shortest_path())}")

    shortest_path = float("inf")
    for start in hill.lowest_nodes():
        path = hill.shortest_path(start)
        if path is not None:
            shortest_path = min(shortest_path, len(path))
    print(f"Part 2: {shortest_path}\n")


solve(sample_input)
solve(actual_input)
