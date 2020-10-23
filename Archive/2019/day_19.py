import logging
import math
import os

from grid_system import XY, ConnectedGrid
from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_19.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_19_input.txt")
with open(file_path) as f:
    program_str = f.read()
program = [int(x) for x in program_str.split(",")]


class DroneSystem(ConnectedGrid):
    def __init__(self, program):
        super().__init__()
        self.program = program

    def test_xy(self, x, y):
        computer = IntCodeComputer(self.program)
        computer.run_program([x, y])
        return computer.output() == [1]

    def picture_50_x_50(self):
        hashes = 0
        for y in range(50):
            for x in range(50):
                c = "."
                if self.test_xy(x, y):
                    c = "#"
                print(c, end="")
            print()

    def find_top_right(self, y):
        guess_x = math.floor(41.0 / 50.0 * y)
        in_beam = self.test_xy(guess_x, y)
        if in_beam:
            search = +1
        else:
            search = -1
        while True:
            print(f"{guess_x},{y} in beam: {in_beam}")
            input()
            if self.test_xy(guess_x + search, y) == (not in_beam):
                break
            guess_x += search
        if in_beam:
            guess_x -= 1
        return XY(guess_x, y)


ds = DroneSystem(program)
print(ds.find_top_right(32))

