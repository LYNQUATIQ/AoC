"""https://adventofcode.com/2018/day/20"""
import os

from collections import deque
from typing import NamedTuple

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day20_input.txt")) as f:
    actual_input = f.read()


sample_input = """^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"""


class XY(NamedTuple("Pt", [("x", int), ("y", int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)


class RegexMaze:
    WALL = "#"
    ROOM = "."
    DOOR = "+"
    UNKNOWN = "?"
    START = "X"

    DIRECTIONS = {"N": XY(0, -1), "S": XY(0, 1), "E": XY(1, 0), "W": XY(-1, 0)}

    GROUP_START = "("
    GROUP_END = ")"
    OPTION = "|"
    TERMINATOR = "$"

    def __init__(self, regex):
        super().__init__()
        self.grid = {}
        self.regex = deque(regex)
        self.start = XY(0, 0)
        self.create_room(self.start)
        self.grid[self.start] = self.START
        xy = self.start
        last_start = [xy]
        while True:
            c = self.regex.popleft()
            if c == self.TERMINATOR:
                break
            if c == self.GROUP_START:
                last_start.append(xy)
                continue
            if c == self.OPTION:
                xy = last_start[-1]
                continue
            if c == self.GROUP_END:
                xy = last_start.pop()
                continue
            direction = self.DIRECTIONS[c]
            xy += direction
            self.grid[xy] = self.DOOR
            xy += direction
            self.create_room(xy)

        for xy, c in self.grid.items():
            if c == self.UNKNOWN:
                self.grid[xy] = self.WALL

    def create_room(self, xy):
        self.grid[xy] = self.ROOM
        for corner in (xy + c for c in (XY(-1, -1), XY(1, -1), XY(1, 1), XY(-1, 1))):
            self.grid[corner] = self.WALL
        for exit in (xy + d for d in (XY(-1, 0), XY(1, 0), XY(0, 1), XY(0, -1))):
            if exit not in self.grid:
                self.grid[exit] = self.UNKNOWN

    def connected_rooms(self, room):
        return [
            room + d + d
            for d in (XY(0, -1), XY(0, 1), XY(1, 0), XY(-1, 0))
            if self.grid[room + d] == self.DOOR
        ]


@print_time_taken
def solve(inputs):
    maze = RegexMaze(inputs[1:])

    # BFS of maze counting doors as we go
    to_visit, visited = [(maze.start, 0)], set()
    max_doors, paths_1000_plus = 0, 0
    while to_visit:
        last_room, doors_so_far = to_visit.pop()
        visited.add(last_room)
        doors_so_far += 1
        next_steps = [n for n in maze.connected_rooms(last_room) if n not in visited]
        for next_step in next_steps:
            to_visit.append((next_step, doors_so_far))
            if doors_so_far >= 1000:
                paths_1000_plus += 1
            max_doors = max(max_doors, doors_so_far)

    print(f"Part 1: {max_doors}")
    print(f"Part 2: {paths_1000_plus}\n")


solve(sample_input)
solve(actual_input)
