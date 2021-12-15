import os
import sys

from heapq import heappush, heappop
from itertools import product, count

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
        risk_level = {xy: sys.maxsize for xy in grid}
        risk_level[start] = 0
        to_visit = []
        heappush(to_visit, (0, start))
        while to_visit:
            risk_to_here, this_node = heappop(to_visit)
            if this_node == target:
                break
            for next_node in (n for n in neighbours(*this_node) if n in grid):
                total_risk_next_node = risk_to_here + grid[next_node]
                if total_risk_next_node < risk_level[next_node]:
                    risk_level[next_node] = total_risk_next_node
                    heappush(to_visit, (total_risk_next_node, next_node))

        return risk_level[target]

    print(f"Part 1: {find_shortest_path(small_grid)}")
    print(f"Part 2: {find_shortest_path(big_grid)}\n")


solve(sample_input)
solve(actual_input)
