import logging
import os

from collections import defaultdict, deque

from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_20.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, f"inputs/2018_day_20_input.txt")
regex = [line.rstrip("\n") for line in open(file_path)][0][1:]


class RegexMaze(ConnectedGrid):
    WALL = "#"
    ROOM = "."
    V_DOOR = "|"
    H_DOOR = "-"
    UNKNOWN = "?"
    START = "X"

    doors = [V_DOOR, H_DOOR]

    regex_directions = {
        "N": (ConnectedGrid.NORTH, H_DOOR),
        "S": (ConnectedGrid.SOUTH, H_DOOR),
        "E": (ConnectedGrid.EAST, V_DOOR),
        "W": (ConnectedGrid.WEST, V_DOOR),
    }

    GROUP_START = "("
    GROUP_END = ")"
    OPTION = "|"

    TEMRINATOR = "$"

    GROUP_TERMINATORS = [GROUP_END, OPTION]

    corners = [XY(-1, -1), XY(1, -1), XY(1, 1), XY(-1, 1)]

    def create_room(self, xy):
        self.grid[xy] = self.ROOM
        for corner in [xy + c for c in self.corners]:
            self.grid[corner] = self.WALL
        for direction in [xy + d for d in self.directions]:
            if self.grid.get(direction, self.UNKNOWN) == self.UNKNOWN:
                self.grid[direction] = self.UNKNOWN

    def __init__(self, regex):
        super().__init__()
        self.regex = deque(regex)
        self.start = XY(0, 0)
        self.rooms = {}
        self.create_room(self.start)
        self.grid[self.start] = self.START
        xy = self.start
        doors = 0
        last_start = [(xy, 0)]
        while True:
            c = self.regex.popleft()
            if c == self.TEMRINATOR:
                break
            if c == self.GROUP_START:
                last_start.append((xy, doors))
                continue
            if c == self.OPTION:
                (xy, doors) = last_start[-1]
                continue
            if c == self.GROUP_END:
                (xy, doors) = last_start.pop()
                continue
            direction, door = self.regex_directions[c]
            xy += direction
            self.grid[xy] = door
            doors += 1
            xy += direction
            self.create_room(xy)
            self.rooms[xy] = doors

        for xy, c in self.grid.items():
            if c == self.UNKNOWN:
                self.grid[xy] = self.WALL

    def connected_rooms(self, room):
        connected_nodes = room.neighbours
        connected_rooms = []
        for direction in self.directions:
            door_xy = room + direction
            if self.grid[door_xy] in self.doors:
                connected_rooms.append(door_xy + direction)
        return connected_rooms


maze = RegexMaze(regex)
# maze.print_grid(margin=1)

# BFS of maze couting doors as we go
walls = [xy for xy, c in maze.grid.items() if c == maze.WALL]
number_of_doors = 0
xy = maze.start
visited = set()
furthest_points = [(xy, 0)]
max_doors = 0
paths_1000_plus = 0
while furthest_points:
    last_room, doors = furthest_points.pop()
    visited.add(last_room)
    doors += 1
    # maze.print_grid(zoom=(last_room, 5))
    next_steps = [n for n in maze.connected_rooms(last_room) if n not in visited]
    for next_step in next_steps:
        furthest_points.append((next_step, doors))
        if doors >= 1000:
            paths_1000_plus += 1
        max_doors = max(max_doors, doors)

print(f"Part 1: {max_doors}")
print(f"Part 2: {paths_1000_plus}")
