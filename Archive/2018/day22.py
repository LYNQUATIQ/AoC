"""https://adventofcode.com/2018/day/22"""
import os
import re

from functools import lru_cache
from heapq import heappush, heappop
from itertools import product

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """depth: 510
target: 10,10"""


class CaveSystem:
    ROCKY, WET, NARROW = 0, 1, 2
    CLIMBING_GEAR, TORCH, NEITHER = 0, 1, 2
    ALLOWED = {
        (ROCKY, CLIMBING_GEAR),
        (ROCKY, TORCH),
        (WET, CLIMBING_GEAR),
        (WET, NEITHER),
        (NARROW, NEITHER),
        (NARROW, TORCH),
    }

    NEIGHBOURS_ALLOWED = {
        (ROCKY, CLIMBING_GEAR): {ROCKY, WET},
        (ROCKY, TORCH): {ROCKY, NARROW},
        (WET, CLIMBING_GEAR): {WET, ROCKY},
        (WET, NEITHER): {WET, NARROW},
        (NARROW, TORCH): {NARROW, ROCKY},
        (NARROW, NEITHER): {NARROW, WET},
    }

    SWITCHES_ALLOWED = {
        (ROCKY, CLIMBING_GEAR): TORCH,
        (ROCKY, TORCH): CLIMBING_GEAR,
        (WET, CLIMBING_GEAR): NEITHER,
        (WET, NEITHER): CLIMBING_GEAR,
        (NARROW, TORCH): NEITHER,
        (NARROW, NEITHER): TORCH,
    }

    def __init__(self, depth: int, target_x: int, target_y: int):
        self.depth = depth
        self.target_x = target_x
        self.target_y = target_y
        self._erosion_level = [[None for _ in range(2000)] for _ in range(1000)]

    def erosion_level(self, x, y):
        if self._erosion_level[x][y] is not None:
            return self._erosion_level[x][y]
        geologic_index = None
        if y == 0:
            geologic_index = x * 16807
        elif x == 0:
            geologic_index = y * 48271
        elif (x, y) == (self.target_x, self.target_y):
            geologic_index = 0
        else:
            geologic_index = self.erosion_level(x - 1, y) * self.erosion_level(x, y - 1)
        erosion_level = (geologic_index + self.depth) % 20183
        self._erosion_level[x][y] = erosion_level
        return erosion_level

    def print_cave_system(self):
        border = 6
        for y in range(self.target_y + border):
            for x in range(self.target_x + border):
                xy = (x, y)
                symbol = {self.ROCKY: ".", self.WET: "=", self.NARROW: "|"}[
                    self.erosion_level(x, y) % 3
                ]
                if (x, y) == (0, 0):
                    symbol = "M"
                elif (x, y) == (self.target_x, self.target_y):
                    symbol = "T"
                print(symbol, end="")
            print()

    def total_risk_level(self):
        return sum(
            self.erosion_level(x, y) % 3
            for x, y in product(range(self.target_x + 1), range(self.target_y + 1))
        )

    def best_route(self):
        current_node = (0, 0, self.TORCH)
        shortest_distance = {current_node: 0}
        to_visit = []
        heappush(to_visit, (0, 0, current_node))
        while True:
            _, cost_to_current_node, current_node = heappop(to_visit)
            if current_node == (self.target_x, self.target_y, self.TORCH):
                return shortest_distance[current_node]
            for next_node, cost in self.next_steps(current_node):
                if next_node in shortest_distance:
                    continue
                cost_to_next_node = cost_to_current_node + cost
                if next_node in shortest_distance:
                    current_shortest_cost = shortest_distance[next_node]
                    if current_shortest_cost < cost_to_next_node:
                        continue
                shortest_distance[next_node] = cost_to_next_node
                nx, ny, gear = next_node
                estimated_cost = (
                    cost_to_next_node
                    + abs(nx - self.target_x)
                    + abs(ny - self.target_y)
                    + 7 * (gear != self.TORCH)
                )
                heappush(to_visit, (estimated_cost, cost_to_next_node, next_node))

    @lru_cache
    def next_steps(self, node):
        x, y, current_gear = node
        region_type = self.erosion_level(x, y) % 3
        neighbours = ((x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)))
        allowed_nodes = set(
            ((nx, ny, current_gear), 1)
            for nx, ny in neighbours
            if 0 <= nx
            and 0 <= ny
            and self.erosion_level(nx, ny) % 3
            in self.NEIGHBOURS_ALLOWED[(region_type, current_gear)]
        )
        allowed_nodes.add(
            ((x, y, self.SWITCHES_ALLOWED[(region_type, current_gear)]), 7)
        )
        return allowed_nodes


@print_time_taken
def solve(inputs):
    depth, t_x, t_y = map(int, re.findall("\d+", inputs))
    caves = CaveSystem(depth, t_x, t_y)
    print(f"Part 1: {caves.total_risk_level()}")
    # caves.print_cave_system()
    print(f"Part 2: {caves.best_route()}")


solve(sample_input)
# solve(actual_input)
