import logging
import os

from collections import Counter, deque
from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)


class Building(ConnectedGrid):

    WALL = "#"
    OPEN_SPACE = "."

    def __init__(self, favourite_number):
        super().__init__()
        self.favourite_number = favourite_number
        self.get_symbol(XY(0, 0))
        self.get_symbol(XY(9, 6))

    def get_symbol(self, xy):
        if xy.x < 0 or xy.y < 0:
            return self.WALL
        try:
            return self.grid[xy]
        except KeyError:
            x, y = xy
            n_bits_odd = (
                Counter(
                    bin(x * x + 3 * x + 2 * x * y + y + y * y + self.favourite_number)[
                        2:
                    ]
                ).get("1", 0)
                % 2
            )
            self.grid[xy] = {0: self.OPEN_SPACE, 1: self.WALL}[n_bits_odd]
        return self.grid[xy]

    def connected_nodes(self, node, blockages=None):
        return [n for n in node.neighbours if self.get_symbol(n) == self.OPEN_SPACE]


b = Building(1364)
start = XY(1, 1)
path = b.find_shortest_path(start, XY(31, 39))
print(f"Part 1: {len(path)}")

print(f"Part 2: {len(b.bfs_paths(start, 50).keys())}")
