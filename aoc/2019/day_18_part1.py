import os
import string

from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "inputs/day_18_input_pt1.txt")
map_image = [line.rstrip("\n") for line in open(file_path)]


class UndergroundCavern(ConnectedGrid):

    SPACE = "."
    WALL = "#"
    START = "@"

    def __init__(self):
        super().__init__()
        self.keys = {}
        self.doors = {}
        self.paths_cache = {}
        self.routes_cache = {}

    def get_symbol(self, xy, char_map={}):
        symbol = super().get_symbol(xy, char_map)
        symbol = {self.WALL: "\u2588"}.get(symbol, symbol)
        if xy in self.keys.keys():
            symbol = self.keys[xy].lower()
        if xy in self.doors.keys():
            format = ";".join([str(0), str(30), str(47)])
            symbol = f"\x1b[{format}m{self.doors[xy]}\x1b[0m"
        if xy in self.start:
            symbol = self.start.index(xy)
        return symbol

    def load_map(self, map_image):
        for y, scan_line in enumerate(map_image):
            for x, c in enumerate(scan_line):
                xy = XY(x, y)
                if c == self.START:
                    self.start = xy
                    c = self.SPACE
                elif c in string.ascii_lowercase:
                    self.keys[xy] = c.upper()
                    c = self.SPACE
                elif c in string.ascii_uppercase:
                    self.doors[xy] = c
                    c = self.SPACE
                self.grid[xy] = c
        self.print_grid()

    def connected_nodes(self, node, blockages=None):
        connected_nodes = [
            n for n in node.neighbours if self.grid.get(n, None) != self.WALL
        ]
        if blockages:
            connected_nodes = [n for n in connected_nodes if n not in blockages]
        return connected_nodes

    def gather_all_paths(self):
        def store_in_cache(start, end, path):
            doors_en_route = []
            keys_en_route = []
            for step in path:
                try:
                    doors_en_route.append(self.doors[step])
                except KeyError:
                    pass
                try:
                    keys_en_route.append(self.keys[step])
                except KeyError:
                    pass
            self.paths_cache[(start, end)] = (len(path), doors_en_route, keys_en_route)

        start_paths = self.paths_to_goals(self.start, self.keys.keys())
        for key, path in start_paths.items():
            store_in_cache(self.START, self.keys[key], path)

        for start, key in self.keys.items():
            other_keys = [k for k in self.keys.keys() if k != start]
            paths = self.paths_to_goals(start, other_keys)
            for other_key, path in paths.items():
                store_in_cache(key, self.keys[other_key], path)

    def paths_to_keys(self, start, keys_to_find):
        paths = {}
        for key in keys_to_find:
            length, doors_en_route, keys_en_route = self.paths_cache[(start, key)]
            if all([(door not in keys_to_find) for door in doors_en_route]):
                paths[key] = (length, keys_en_route)
        return paths

    def find_route_from_node(self, start=None, keys_to_find=None):

        if start is None:
            start = self.START

        if keys_to_find is None:
            keys_to_find = "".join(key for key in sorted(self.keys.values()))

        if not keys_to_find:
            return (0, [])

        branches = self.paths_to_keys(start, keys_to_find).items()
        best_branch = None
        best_route = None
        shortest_distance = None
        for next_key, (distance, keys_en_route) in branches:
            next_keys_to_find = "".join(
                k for k in keys_to_find if k not in keys_en_route
            )
            try:
                route_from_here = self.routes_cache[(next_key, next_keys_to_find)]
            except KeyError:
                route_from_here = self.find_route_from_node(next_key, next_keys_to_find)
                self.routes_cache[(next_key, next_keys_to_find)] = route_from_here
            if route_from_here:
                (route_length, route) = route_from_here
                if best_route is None or route_length + distance < shortest_distance:
                    best_route = [k for k in keys_en_route if k not in route] + route
                    shortest_distance = route_length + distance

        if best_route:
            best_route = (shortest_distance, best_route)

        return best_route


uc = UndergroundCavern()
uc.load_map(map_image)
uc.gather_all_paths()
distance, route = uc.find_route_from_node()
print(f"Part 1: {distance}")
