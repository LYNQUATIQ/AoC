import logging
import os

from itertools import permutations
from grid_system import ConnectedGrid, XY


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Hvac(ConnectedGrid):
    WALL = "#"
    CORRIDOR = "."

    def __init__(self, lines):
        super().__init__()
        self.goals = {}
        self.paths = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                xy = XY(x, y)
                if c not in [self.WALL, self.CORRIDOR]:
                    self.goals[int(c)] = xy
                self.grid[xy] = c
                x += 1
            y += 1
        self.num_goals = len(self.goals)

    def connected_nodes(self, node, blockages=None):
        return [n for n in node.neighbours if self.grid[n] != self.WALL]

    def shortest_path(self, a, b):
        try:
            return self.paths[(a, b)]
        except KeyError:
            pass
        path = self.find_shortest_path(a, b)
        self.paths[(a, b)] = path
        self.paths[(b, a)] = path
        return path

    def best_route(self, return_to_0=False):
        best_path = None
        for route in permutations(range(self.num_goals)):
            route = list(route)
            if route[0] != 0:
                continue
            if return_to_0:
                route.append(0)
            full_path = []
            last_goal = 0
            for next_goal in route[1:]:
                if next_goal != 0 and self.goals[next_goal] in full_path:
                    continue
                path = self.shortest_path(self.goals[last_goal], self.goals[next_goal])
                full_path.extend(path)
                last_goal = next_goal
            if best_path is None or len(full_path) < len(best_path):
                best_path = full_path
        return best_path


hvac = Hvac(lines)
print(f"Part 1 : {len(hvac.best_route())}")
print(f"Part 2 : {len(hvac.best_route(return_to_0=True))}")

