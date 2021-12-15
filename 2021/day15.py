import os
import sys

from itertools import product

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day15_input.txt")) as f:
    actual_input = f.read()

sample_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


@print_time_taken
def solve(inputs):
    small_grid = {
        (x, y): int(height)
        for y, line in enumerate(inputs.splitlines())
        for x, height in enumerate(line)
    }

    w, h = (max(xy[0] for xy in small_grid) + 1, max(xy[1] for xy in small_grid) + 1)
    big_grid = {}
    for dx, dy in product(range(5), range(5)):
        for xy, risk in small_grid.items():
            big_grid[(xy[0] + dx * w, xy[1] + dy * h)] = (risk - 1 + dx + dy) % 9 + 1

    neighbours = lambda x, y: ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))

    def find_shortest_path(grid):
        start, target = (0, 0), (max(xy[0] for xy in grid), max(xy[1] for xy in grid))
        to_visit = {start: 0}
        total_risk_levels = dict()
        while to_visit:
            current_node = min(to_visit, key=to_visit.get)
            grid.pop(current_node)
            risk_to_here = to_visit.pop(current_node)
            total_risk_levels[current_node] = risk_to_here
            if current_node == target:
                break
            for next_node in (n for n in neighbours(*current_node) if n in grid):
                total_risk_to_next_node = grid[next_node] + risk_to_here
                if total_risk_to_next_node < to_visit.get(next_node, sys.maxsize):
                    to_visit[next_node] = total_risk_to_next_node

        return total_risk_levels[target]

    print(f"Part 1: {find_shortest_path(small_grid)}")
    print(f"Part 2: {find_shortest_path(big_grid)}\n")


solve(sample_input)
solve(actual_input)
