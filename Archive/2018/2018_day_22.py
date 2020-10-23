import logging
import os
import re

from functools import lru_cache

from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_22.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)


class CaveSystem:
    ROCKY = "."
    WET = "="
    NARROW = "|"

    MOUTH = "M"
    TARGET = "T"

    CLIMBING_GEAR = "Climbing Gear"
    TORCH = "Torch"
    NEITHER = "Neither"

    neighbours_allowed = {
        (ROCKY, CLIMBING_GEAR): set([ROCKY, WET]),
        (ROCKY, TORCH): set([ROCKY, NARROW]),
        (WET, CLIMBING_GEAR): set([WET, ROCKY]),
        (WET, NEITHER): set([WET, NARROW]),
        (NARROW, TORCH): set([NARROW, ROCKY]),
        (NARROW, NEITHER): set([NARROW, WET]),
    }

    switches_allowed = {
        (ROCKY, CLIMBING_GEAR): TORCH,
        (ROCKY, TORCH): CLIMBING_GEAR,
        (WET, CLIMBING_GEAR): NEITHER,
        (WET, NEITHER): CLIMBING_GEAR,
        (NARROW, TORCH): NEITHER,
        (NARROW, NEITHER): TORCH,
    }

    def __init__(self, depth=10914, target=XY(9, 739)):
        super().__init__()
        self.depth = depth
        self.target = target
        self.mouth = XY(0, 0)
        self.geological_indices = {self.mouth: 0, self.target: 0}

    def print_cave_system(self, print_header=False, margin=0, zoom=None):
        max_beyond = 6
        for y in range(self.target.y + max_beyond):
            for x in range(self.target.x + max_beyond):
                xy = XY(x, y)
                if xy == self.mouth:
                    symbol = self.MOUTH
                elif xy == self.target:
                    symbol = self.TARGET
                else:
                    symbol = self.region_type(xy)
                print(symbol, end="")
            print()

    def best_route(self):
        current_node = (self.mouth, self.TORCH)
        shortest_paths = {current_node: (None, 0)}
        visited = set()

        while current_node != (self.target, self.TORCH):
            visited.add(current_node)
            _, cost_to_current_node = shortest_paths[current_node]
            for xy, equipped, cost in self.allowed_nodes(current_node):
                next_node = (xy, equipped)
                cost_to_next_node = cost_to_current_node + cost
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (
                        current_node,
                        cost_to_next_node,
                    )
                else:
                    _, current_shortest_cost = shortest_paths[next_node]
                    if current_shortest_cost > cost_to_next_node:
                        shortest_paths[next_node] = (current_node, cost_to_next_node)

            next_destinations = {
                node: shortest_paths[node]
                for node in shortest_paths
                if node not in visited
            }
            if not next_destinations:
                raise Exception

            # next node is the destination with the lowest cost
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        cost = shortest_paths[current_node][1]
        path = []
        xy, equipped
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]

        return cost, path

    @lru_cache
    def allowed_nodes(self, node):
        xy, equipped = node
        neighbours = self.neighbours(xy)
        xy_region_type = self.region_type(xy)
        allowed_neighbours = self.neighbours_allowed[(xy_region_type, equipped)]
        allowed_nodes = [
            (move, equipped, 1)
            for move in neighbours
            if self.region_type(move) in allowed_neighbours
        ]
        allowed_switch = self.switches_allowed[(xy_region_type, equipped)]
        allowed_nodes.append((xy, allowed_switch, 7))
        return allowed_nodes

    @lru_cache
    def neighbours(self, xy):
        neighbours = []
        max_beyond = 100
        for direction in [XY(0, 1), XY(1, 0), XY(0, -1), XY(-1, 0)]:
            n = xy + direction
            if (
                n.x >= 0
                and n.y >= 0
                and n.x <= self.target.x + max_beyond
                and n.y <= self.target.y + max_beyond
            ):
                neighbours.append(n)
        return neighbours

    def total_risk_level(self):
        total_risk_level = 0
        for y in range(self.target.y + 1):
            for x in range(self.target.x + 1):
                total_risk_level += self.risk_level(XY(x, y))
        return total_risk_level

    @lru_cache
    def risk_level(self, xy):
        return self.erosion_level(xy) % 3

    @lru_cache
    def region_type(self, xy):
        region_type = self.erosion_level(xy) % 3
        if region_type == 0:
            return self.ROCKY
        elif region_type == 1:
            return self.WET
        else:
            return self.NARROW

    @lru_cache
    def erosion_level(self, xy):
        return (self.geological_index(xy) + self.depth) % 20183

    @lru_cache
    def geological_index(self, xy):
        try:
            return self.geological_indices[xy]
        except KeyError:
            pass
        if xy.y == 0:
            self.geological_indices[xy] = xy.x * 16807
        elif xy.x == 0:
            self.geological_indices[xy] = xy.y * 48271
        else:
            xy1 = XY(xy.x - 1, xy.y)
            xy2 = XY(xy.x, xy.y - 1)
            self.geological_indices[xy] = self.erosion_level(xy1) * self.erosion_level(
                xy2
            )
        return self.geological_indices[xy]


caves = CaveSystem()
print(caves.total_risk_level())
caves.print_cave_system()
cost, path = caves.best_route()
print(path)
print(cost)
