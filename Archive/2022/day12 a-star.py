"""https://adventofcode.com/2022/day/12"""
from __future__ import annotations
import os

from heapq import heappop, heappush
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
                target, elevation = xy, 25
            grid[xy] = elevation

    possible_steps = {
        xy: tuple([n for n in xy.neighbours if grid.get(n, 999) - grid[xy] <= 1])
        for xy in grid
    }
    distance_to_target = {
        xy: abs(target.x - xy.x) + abs(target.x - xy.x) for xy in grid
    }

    def shortest_path(starts: list[XY]) -> int:
        visited: set[XY] = set()
        distance_to = {start: 0 for start in starts}
        to_visit: list[tuple[float, XY]] = []
        for start in starts:
            heappush(to_visit, (distance_to_target[start], start))
        while to_visit:
            _, this_node = heappop(to_visit)
            if this_node == target:
                return distance_to[this_node]
            visited.add(this_node)
            for next_step in possible_steps[this_node]:
                distance_to_here = distance_to[this_node] + 1
                prior_distance_to_here = distance_to.get(next_step, 0)
                if next_step in visited and distance_to_here >= prior_distance_to_here:
                    continue
                if distance_to_here < prior_distance_to_here or next_step not in [
                    i[1] for i in to_visit
                ]:
                    distance_to[next_step] = distance_to_here
                    f_score = distance_to_here + distance_to_target[next_step]
                    heappush(to_visit, (f_score, next_step))
        raise ValueError("No path found")

    possible_starts = list(
        {
            s
            for s, e in grid.items()
            if e == 1 and any(grid[n] == 0 for n in possible_steps[s])
        }
    )

    print(f"Part 1: {shortest_path([start])}")
    print(f"Part 2: {shortest_path(possible_starts)+1}\n")


solve(sample_input)
solve(actual_input)
