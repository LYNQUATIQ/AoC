# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
from itertools import product

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day15.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
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
    grid = {
        (x, y): int(height)
        for y, line in enumerate(inputs.splitlines())
        for x, height in enumerate(line)
    }
    neighbours = lambda x, y: ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))

    start = (0, 0)
    target = (max(xy[0] for xy in grid), max(xy[1] for xy in grid))

    def find_shortest_path(grid, start, target):
        # best_paths is a dict of nodes mapped to a tuple of (previous node, risk_level)
        best_paths = {start: (None, 0)}
        current_node = start
        visited = set()
        while current_node != target:
            visited.add(current_node)
            next_nodes = tuple(xy for xy in neighbours(*current_node) if xy in grid)
            risk_level_to_here = best_paths[current_node][1]
            for next_node in next_nodes:
                risk_level = grid[next_node] + risk_level_to_here
                if next_node not in best_paths:
                    best_paths[next_node] = (current_node, risk_level)
                else:
                    current_lowest_risk_level = best_paths[next_node][1]
                    if current_lowest_risk_level > risk_level:
                        best_paths[next_node] = (current_node, risk_level)

            next_steps = {
                node: best_paths[node] for node in best_paths if node not in visited
            }
            if not next_steps:
                raise ValueError("No path possible")
            # next node is the destination with the lowest risk_level
            current_node = min(next_steps, key=lambda k: next_steps[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = best_paths[current_node][0]
            current_node = next_node
        return path[:-1]

    total_risk_level = sum(grid[xy] for xy in find_shortest_path(grid, start, target))
    print(f"Part 1: {total_risk_level}")

    big_grid = {}
    for my in range(5):
        for mx in range(5):
            for xy, risk_level in grid.items():
                big_grid[
                    (xy[0] + mx * (target[0] + 1), xy[1] + my * (target[1] + 1))
                ] = (risk_level - 1 + mx + my) % 9 + 1

    target = (target[0] * 5, target[1] * 5)

    total_risk_level = sum(
        big_grid[xy] for xy in find_shortest_path(big_grid, start, target)
    )
    print(f"Part 2: {total_risk_level}\n")


solve(sample_input)
# solve(actual_input)
