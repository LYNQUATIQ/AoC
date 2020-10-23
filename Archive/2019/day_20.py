import logging
import os
import string

from collections import defaultdict, deque
from itertools import combinations

from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_20_log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)


class XYLevel:
    def __init__(self, xy, level):
        self.xy = xy
        self.level = level

    def __hash__(self):
        return self.xy.__hash__() * 1000 + self.level

    def __repr__(self):
        return f"{self.xy}({self.level})"

    def __eq__(self, value):
        return self.xy == value.xy and self.level == value.level


class PlutoMaze(ConnectedGrid):

    VACUUM = " "
    PATH = "."
    WALL = "#"

    MAX_LEVEL = 30

    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None
        self.portals = {}  # Portal locations -> (portal exit location, level change)

    def get_symbol(self, xy):
        symbol = super().get_symbol(xy)
        symbol = {self.WALL: "\u2588"}.get(symbol, symbol)
        return symbol

    def load_map(self, map_image):
        for y, scan_line in enumerate(map_image):
            for x, c in enumerate(scan_line):
                xy = XY(x, y)
                self.grid[xy] = c

        self.print_grid()

    def hook_up_portals(self):

        partial_portals = {}

        # Find portals
        min_x, min_y, max_x, max_y = self.get_limits()
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                xy = XY(x, y)
                if self.grid.get(xy, None) != self.PATH:
                    continue
                for direction in self.directions:
                    if self.grid[xy + direction] not in string.ascii_uppercase:
                        continue
                    portal_xy = xy + direction
                    portal_xy2 = portal_xy + direction
                    c1 = self.grid[portal_xy]
                    c2 = self.grid[portal_xy2]
                    if direction in [self.NORTH, self.WEST]:
                        portal = c2 + c1
                    else:
                        portal = c1 + c2
                    if portal == "AA":
                        self.start = xy
                        self.grid[portal_xy] = self.WALL
                        self.grid[portal_xy2] = self.WALL
                        continue
                    if portal == "ZZ":
                        self.end = xy
                        self.grid[portal_xy] = self.WALL
                        self.grid[portal_xy2] = self.WALL
                        continue
                    try:
                        portal_pair_xy, pair_xy = partial_portals[portal]
                        level_change = +1
                        if any(
                            [
                                portal_xy.x < min_x + 2,
                                portal_xy.x > max_x - 3,
                                portal_xy.y < min_y + 2,
                                portal_xy.y > max_y - 3,
                            ]
                        ):
                            level_change = -1
                        self.portals[portal_pair_xy] = (xy, level_change * -1)
                        self.portals[portal_xy] = (pair_xy, level_change)
                        del partial_portals[portal]
                    except KeyError:
                        partial_portals[portal] = (portal_xy, xy)

    def next_steps(self, xyl):
        next_steps = []
        for xy in xyl.xy.neighbours:
            c = self.grid.get(xy, None)
            if c == self.WALL:
                continue
            elif c == self.PATH:
                next_steps.append((XYLevel(xy, xyl.level)))
            elif c in string.ascii_uppercase:
                portal_exit, level_change = self.portals[xy]
                if (xyl.level + level_change) in range(0, self.MAX_LEVEL):
                    next_steps.append(XYLevel(portal_exit, xyl.level + level_change))
        return next_steps

    def shortest_path(self, start_xy, end_xy):
        start = XYLevel(start_xy, 0)
        end = XYLevel(end_xy, 0)
        paths = {start: None}
        distances = {start: 0}

        # List of points (xylevel) to visit (and their distance from the start)
        to_visit = deque([(start, 0)])
        visited = set()

        while to_visit:
            xyl, distance_so_far = to_visit.popleft()
            for next_step in self.next_steps(xyl):

                if next_step not in paths or distances[next_step] > (
                    distance_so_far + 1
                ):
                    paths[next_step] = xyl
                    distances[next_step] = distance_so_far + 1
                if next_step in visited:
                    continue
                if next_step in [q for q, _ in to_visit]:
                    continue
                to_visit.append((next_step, distance_so_far + 1))
            visited.add(xyl)

        try:
            step = paths[end]
            distance = distances[end]
        except KeyError:
            return None

        path = [end]
        while distance > 1:
            path = [step] + path
            step = paths[step]
            distance = distances[step]

        return path


file_path = os.path.join(script_dir, "inputs/day_20_input.txt")
map_image = [line.rstrip("\n") for line in open(file_path)]

maze = PlutoMaze()
maze.load_map(map_image)
maze.hook_up_portals()
path = maze.shortest_path(maze.start, maze.end)
if path is None:
    print("Failed :(")
else:
    print(path)
    print(f"{len(path)+1} steps")
