import os

from grid import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


class ChairSystem:
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"

    def __repr__(self):
        s = ""
        for y in range(self.max_y):
            for x in range(self.max_x):
                xy = XY(x, y)
                c = self.FLOOR
                if XY(x, y) in self.chairs:
                    c = self.EMPTY
                    if XY(x, y) in self.occupied:
                        c = self.OCCUPIED
                s += c
            s += "\n"
        s += "\n"
        return s

    def __init__(self, inputs, tolerance=4, immediate_neighbours_only=True):
        self.tolerance = tolerance
        self.immediate_neighbours_only = immediate_neighbours_only

        self.chairs = set()
        self.occupied = set()

        self.max_x, self.max_y = None, None
        for y, line in enumerate(inputs.split()):
            for x, c in enumerate(line):
                if c != self.FLOOR:
                    chair = XY(x, y)
                    self.chairs.add(chair)
                    if c == self.OCCUPIED:
                        self.occupied.add(chair)
                self.max_x = x + 1
            self.max_y = y + 1

    def occupied_chairs_in_sight(self, this_chair):
        occupied_chairs_in_sight = 0
        for direction in XY.all_directions():
            xy = this_chair
            while True:
                xy += direction
                if xy.x < 0 or xy.x >= self.max_x or xy.y < 0 or xy.y >= self.max_y:
                    break
                if xy in self.chairs:
                    occupied_chairs_in_sight += xy in self.occupied
                    break
                if self.immediate_neighbours_only:
                    break
        return occupied_chairs_in_sight

    def iterate(self):
        new_occupied = set()
        for chair in self.chairs:
            neighbour_count = self.occupied_chairs_in_sight(chair)
            if chair not in self.occupied:
                if neighbour_count == 0:
                    new_occupied.add(chair)
            else:
                if neighbour_count < self.tolerance:
                    new_occupied.add(chair)
        self.occupied = new_occupied
        return frozenset(self.occupied)

    def find_stable_state(self):
        while True:
            prior_state = frozenset(self.occupied)
            new_state = self.iterate()
            if new_state == prior_state:
                break
        return len(self.occupied)


def solve(inputs):
    chairs = ChairSystem(inputs, tolerance=4, immediate_neighbours_only=True)
    print(f"Part 1: {chairs.find_stable_state()}")
    chairs = ChairSystem(inputs, tolerance=5, immediate_neighbours_only=False)
    print(f"Part 2: {chairs.find_stable_state()}\n")


solve(sample_input)
solve(actual_input)
