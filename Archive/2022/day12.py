"""https://adventofcode.com/2022/day/12"""
from __future__ import annotations
import os

from collections import deque

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


@print_time_taken
def solve(inputs: str) -> None:
    start, target = complex(0, 0), complex(0, 0)
    grid: dict[complex, int] = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            xy, elevation = complex(x, y), ord(c) - ord("a")
            if c == "S":
                start, elevation = xy, 0
            elif c == "E":
                target, elevation = xy, 26
            grid[xy] = elevation

    def shortest_path(starts: list[complex]) -> int:
        queue = deque(starts)
        distance_to = {s: 0 for s in starts}
        while queue:
            node = queue.popleft()
            if node == target:
                return distance_to[node]
            for next_node in (
                node + d
                for d in (1, -1, 1j, -1j)
                if grid.get(node + d, 999) - grid[node] <= 1
            ):
                if next_node not in distance_to:
                    queue.append(next_node)
                    distance_to[next_node] = distance_to[node] + 1
        raise ValueError("No path found")

    print(f"Part 1: {shortest_path([start])}")

    possible_starts = list(
        {
            s
            for s, e in grid.items()
            if e == 1 and any(grid.get(s + d, 999) == 0 for d in (1, -1, 1j, -1j))
        }
    )
    print(f"Part 2: {shortest_path(possible_starts)+1}\n")


solve(sample_input)
solve(actual_input)
