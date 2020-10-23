from abc import ABC, abstractmethod
from collections import deque
from typing import NamedTuple

from intcode_computer import IntCodeComputer


class Coord(NamedTuple("Coord", [("x", int), ("y", int)])):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    directions = {
        NORTH: Coord(0, 1),
        EAST: Coord(1, 0),
        SOUTH: Coord(0, -1),
        WEST: Coord(-1, 0),
    }

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def get_direcion(self, neighbour):
        for direction, d in self.directions.items():
            if self + d == neighbour:
                return direction
        return None

    @property
    def neighbours(self):
        return [self + d for d in directions.values()]


class ConnectedGrid(ABC):
    def __init__(self):
        self.grid = {}

    @abstractmethod
    def connected_nodes(self, node):
        pass

    # Find the shortest path to the (closest of) goal(s)
    def shortest_path(self, start, goals):
        if not isinstance(goals, list):
            goals = [goals]
        # List of points to visit (and their distance from the start)
        queued_nodes = deque([(start, 0)])

        # Store paths - for a given node store distance, previous node (as tuple)
        paths = {start: (0, None)}
        visited = set()

        while queued_nodes:
            node, distance = queued_nodes.popleft()
            for neighbour in self.connected_nodes(node):
                if neighbour not in paths or paths[neighbour] > (distance + 1, node):
                    paths[node] = (distance + 1, node)
                if neighbour in visited:
                    continue
                if neighbour not in [q for q, _ in queued_nodes]:
                    queued_nodes.append((neighbour, distance + 1))
            visited.add(node)

        try:
            shortest_distance, closest_goal = min(
                (distance, node)
                for node, (distance, parent) in paths.items()
                if node in goals
            )
        except ValueError:
            return None

        path = []
        distance, node = paths[closest_goal]
        while distance > 1:
            path = [node] + path
            distance, node = paths[closest_goal]

        return path


class OxygenSystemNotFound(Exception):
    pass


class OxygenSystemSearch(ConnectedGrid):
    OPEN = 0
    WALL = 1
    OXYGEN_SYSTEM = 2

    MOVE_NORTH = 1
    MOVE_SOUTH = 2
    MOVE_WEST = 3
    MOVE_EAST = 4

    instructious = {
        Coord.NORTH: MOVE_NORTH,
        Coord.SOUTH: MOVE_SOUTH,
        Coord.EAST: MOVE_EAST,
        Coord.WEST: MOVE_WEST,
    }

    def __init__(self, program):
        super().__init__()
        self.computer = IntCodeComputer(program)

        self.robot = Coord(0, 0)
        self.oxygen_system = None
        self.grid[self.robot] = self.OPEN
        self.to_visit = [loc for loc in self.robot.neighbours]

    @abstractmethod
    def connected_nodes(self, node):
        return [loc for loc in loc.neighbours if self.grid.get(loc, None) == self.OPEN]

    def search(self):
        while not self.oxygen_system:

            if not self.to_visit:
                raise OxygenSystemNotFound

            shortest_path = self.shortest_path(self.robot, self.to_visit)

            if not shortest_path:
                raise OxygenSystemNotFound

            self.try_move(shortest_path[0])

    def try_move(self, new_location):
        direction = self.instructions[self.robot.get_direcion(new_location)]

        self.computer.run_program([direction])
        output = self.computer.last_output()
        if output == 0:
            self.grid[new_location] = self.WALL
            return

        self.move_robot(new_location)
        if output == 2:
            self.oxygen_system = new_location
        self.robot += direction

