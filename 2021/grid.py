from __future__ import annotations
import math
from typing import Dict, Iterator, List, Optional, Tuple, Union

from collections import deque
from functools import lru_cache
from itertools import product


@lru_cache
def _direction_vectors(dimensions: int):
    return list(product((-1, 0, 1), repeat=dimensions))


class Point(tuple):
    def __new__(cls, *_tuple):
        return tuple.__new__(cls, _tuple)

    def __add__(self, other: Point):
        return type(self)(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other: Point):
        return type(self)(*(a - b for a, b in zip(self, other)))

    @property
    def all_neighbours(self):
        for direction in _direction_vectors(len(self)):
            if not all(d == 0 for d in direction):
                yield self + type(self)(*direction)

    @property
    def neighbours(self):
        for direction in _direction_vectors(len(self)):
            if sum(abs(d) for d in direction) == 1:
                yield self + type(self)(*direction)

    @property
    def manhattan_distance(self):
        return sum(abs(d) for d in self)


class XY(Point):
    @classmethod
    def direction(cls, direction: str):
        return {
            "N": cls(0, -1),
            "S": cls(0, 1),
            "E": cls(1, 0),
            "W": cls(-1, 0),
        }[direction.upper()[0]]

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @classmethod
    def directions(cls) -> Iterator[Point]:
        return (cls(*xy) for xy in product((-1, 0, 1), (-1, 0, 1)) if xy != (0, 0))

    def in_bounds(self, *args) -> bool:
        bounds = []
        for arg in args:
            if isinstance(arg, tuple):
                bounds += arg
            else:
                bounds += [arg]
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        if len(bounds) == 1:
            max_x, max_y = bounds[0], bounds[0]
        if len(bounds) == 2:
            max_x, max_y = bounds[0], bounds[1]
        elif len(bounds) == 4:
            min_x, min_y, max_x, max_y = bounds[0], bounds[1], bounds[2], bounds[3]
        return (min_x <= self.x <= max_x) and (min_y <= self.y <= max_y)


Direction = XY


class ConnectedGrid:

    NORTH = XY(0, -1)
    SOUTH = XY(0, 1)
    EAST = XY(1, 0)
    WEST = XY(0, 1)

    def __init__(self):
        self.grid = {}

    def get_limits(self) -> Tuple[int, int, int, int]:
        min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf
        for pt in self.grid.keys():
            min_x = min(min_x, pt.x)
            min_y = min(min_y, pt.y)
            max_x = max(max_x, pt.x + 1)
            max_y = max(max_y, pt.y + 1)
        return min_x, min_y, max_x, max_y

    def get_symbol(self, xy: XY) -> str:
        return self.grid.get(xy, " ")

    def print_grid(self, show_headers: bool = True) -> None:
        min_x, min_y, max_x, max_y = self.get_limits()
        header1 = "     " + "".join(
            [" " * 9 + str(x + 1) for x in range((max_x - 1) // 10)]
        )
        header2 = "    " + "".join([str(x % 10) for x in range(max_x)])
        if show_headers:
            print(header1)
            print(header2)
        for y in range(min_y, max_y):
            if show_headers:
                print(f"{y:3d} ", end="")
            for x in range(min_x, max_x):
                print(self.get_symbol(XY(x, y)), end="")
            if show_headers:
                print(f" {y:<3d} ", end="")
            print()
        if show_headers:
            print(header2)
            print(header1)

    def turn_left(self, facing: Direction) -> Direction:
        return {
            self.NORTH: self.WEST,
            self.WEST: self.SOUTH,
            self.SOUTH: self.EAST,
            self.EAST: self.NORTH,
        }[facing]

    def turn_right(self, facing: Direction) -> Direction:
        return {
            self.NORTH: self.EAST,
            self.EAST: self.SOUTH,
            self.SOUTH: self.WEST,
            self.WEST: self.NORTH,
        }[facing]

    def connected_nodes(self, node, blockages=None) -> Iterator[XY]:
        connected_nodes = node.neighbours
        if blockages:
            connected_nodes = (n for n in connected_nodes if n not in blockages)
        return connected_nodes

    # Breadth first search returning all paths
    def bfs_paths(
        self, start: XY, max_steps=None
    ) -> Dict[XY, Tuple[int, Optional[XY]]]:
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
    def paths_to_goals(
        self, start: XY, goals: List[XY], blockages: Optional[List[XY]] = None
    ) -> Optional[Dict[XY, List[XY]]]:
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
    def find_shortest_path(
        self, start, goals: Union[XY, List[XY]], blockages: Optional[List[XY]] = None
    ) -> Optional[List[XY]]:
        if isinstance(goals, XY):
            goals = [goals]

        paths_to_goals = self.paths_to_goals(start, goals, blockages)

        if not paths_to_goals:
            return None

        best_path = None
        for path in paths_to_goals.values():
            if not best_path or len(path) < len(best_path):
                best_path = path

        return best_path
