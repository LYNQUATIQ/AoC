"""https://adventofcode.com/2022/day/12"""
from __future__ import annotations
import os

from collections import deque
from typing import NamedTuple

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class XY(NamedTuple):
    x: int
    y: int

    @property
    def neighbours(self) -> tuple[XY, XY, XY, XY]:
        return (
            XY(self.x + 1, self.y),
            XY(self.x, self.y + 1),
            XY(self.x - 1, self.y),
            XY(self.x, self.y - 1),
        )


@print_time_taken
def solve(inputs: str) -> None:
    start, target = XY(0, 0), XY(0, 0)
    grid: dict[XY, int] = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            xy, elevation = XY(x, y), ord(c) - ord("a")
            if c == "S":
                start, elevation = xy, 0
            elif c == "E":
                target, elevation = xy, 26
            grid[xy] = elevation

    possible_steps_up = {
        xy: [n for n in xy.neighbours if grid.get(n, 999) - grid[xy] <= 1]
        for xy in grid
    }

    possible_steps_down = {
        xy: [n for n in xy.neighbours if grid.get(n, -999) - grid[xy] >= -1]
        for xy in grid
    }

    def shortest_path(start: XY, target_elevation: int, possible_steps) -> int:
        to_visit: deque[tuple[XY, list]] = deque([(start, [])])
        visited: set[XY] = set()
        while to_visit:
            this_node, path = to_visit.popleft()
            visited.add(this_node)
            if grid[this_node] == target_elevation:
                return len(path)
            for next_node in possible_steps[this_node]:
                if not next_node in visited:
                    to_visit.append((next_node, path + [next_node]))

        raise ValueError("No path found")

    print(f"Part 1: {shortest_path(start, 26,possible_steps_up)}")
    print(f"Part 2: {shortest_path(target, 0, possible_steps_down)}\n")


solve(sample_input)
solve(actual_input)
