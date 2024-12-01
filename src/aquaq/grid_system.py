import logging
import os

from collections import deque
from typing import NamedTuple


class XY(NamedTuple("XY", [("x", int), ("y", int)])):
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    @property
    def neighbours(self):
        return [self + d for d in [XY(0, -1), XY(1, 0), XY(0, 1), XY(-1, 0)]]

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


class ConnectedGrid:

    NORTH = XY(0, -1)
    SOUTH = XY(0, 1)
    EAST = XY(1, 0)
    WEST = XY(-1, 0)
    DIRECTIONS = [NORTH, SOUTH, EAST, WEST]

    def __init__(self):
        self.grid = {}

    def get_limits(self):
        if not self.grid:
            return range(0), range(0)
        min_x, min_y = None, None
        max_x, max_y = None, None
        for pt in self.grid.keys():
            if min_x is None:
                min_x, min_y = pt.x, pt.y
                max_x, max_y = pt.x, pt.y
            min_x = min(min_x, pt.x)
            min_y = min(min_y, pt.y)
            max_x = max(max_x, pt.x + 1)
            max_y = max(max_y, pt.y + 1)
        return min_x, min_y, max_x, max_y

    def get_symbol(self, xy):
        return self.grid.get(xy, " ")

    def print_grid(self):
        min_x, min_y, max_x, max_y = self.get_limits()
        header1 = "     " + "".join([" " * 9 + str(x + 1) for x in range(max_x // 10)])
        header2 = "    " + "".join([str(x % 10) for x in range(max_x)])
        print(header1)
        print(header2)
        for y in range(min_y, max_y):
            print(f"{y:3d} ", end="")
            for x in range(min_x, max_x):
                print(self.get_symbol(XY(x, y)), end="")
            print(f" {y:<3d} ")
        print(header2)
        print(header1)

    def turn_left(self, facing):
        return {
            self.NORTH: self.WEST,
            self.WEST: self.SOUTH,
            self.SOUTH: self.EAST,
            self.EAST: self.NORTH,
        }[facing]

    def turn_right(self, facing):
        return {
            self.NORTH: self.EAST,
            self.EAST: self.SOUTH,
            self.SOUTH: self.WEST,
            self.WEST: self.NORTH,
        }[facing]

    def connected_nodes(self, node, blockages=None):
        connected_nodes = node.neighbours
        if blockages:
            connected_nodes = [n for n in connected_nodes if n not in blockages]
        return connected_nodes

    # Breadth first search returning all paths
    def bfs_paths(self, start, max_steps=None):
        bfs_paths = {start: (0, None)}
        # List of points to visit (and their distance from the start)
        to_visit = deque([(start, 0)])
        visited = set()
        while to_visit:
            this_node, distance_so_far = to_visit.popleft()
            if max_steps is None or distance_so_far < max_steps:
                for next_step in self.connected_nodes(this_node):
                    if next_step not in bfs_paths or bfs_paths[next_step] > (
                        distance_so_far + 1,
                        this_node,
                    ):
                        bfs_paths[next_step] = (distance_so_far + 1, this_node)
                    if next_step in visited:
                        continue
                    if next_step in [q for q, _ in to_visit]:
                        continue
                    to_visit.append((next_step, distance_so_far + 1))
            visited.add(this_node)

        return bfs_paths

    # Find the shortest paths to all the goals
    def paths_to_goals(self, start, goals, blockages=None):
        paths = self.bfs_paths(start)
        paths_to_goals = {}
        for destination, path in paths.items():
            if destination not in goals:
                continue
            path = [destination]
            distance, node = paths[destination]
            while distance > 1:
                path = [node] + path
                distance, node = paths[node]
            paths_to_goals[destination] = path

        if not paths_to_goals:
            return None

        return paths_to_goals

    # Find the shortest path to the closest goal
    def find_shortest_path(self, start, goals, blockages=None):
        if isinstance(goals, XY):
            goals = [goals]

        paths_to_goals = self.paths_to_goals(start, goals, blockages)

        if not paths_to_goals:
            return None

        best_path = None
        for path in paths_to_goals.values():
            if not best_path or len(path) < len(best_path):
                best_path = path

        return path
