import os

from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "inputs/day_19_input.txt")
with open(file_path) as f:
    program_str = f.read()
program = [int(x) for x in program_str.split(",")]


class DroneSystem:
    def __init__(self, program):
        super().__init__()
        self.program = program

    def in_beam(self, x, y):
        computer = IntCodeComputer(self.program)
        computer.run_program([x, y])
        return computer.output() == [1]

    def picture_50_x_50(self):
        hashes = 0
        for y in range(50):
            for x in range(50):
                in_beam = self.in_beam(x, y)
                # print("#" if in_beam else ".", end="")
                hashes += in_beam
            # print()
        return hashes

    def find_100_x_100(self, start_y=1000):
        y = start_y
        x = y * 30 // 50

        assert not self.in_beam(x, y)
        # Find edge
        x += 1
        while not self.in_beam(x, y):
            x += 1

        assert not self.in_beam(x + 99, y - 99)
        # Move down
        while not self.in_beam(x + 99, y - 99):
            y += 1
            while not self.in_beam(x, y):
                x += 1

        return 10000 * x + y - 99


ds = DroneSystem(program)
hashes = ds.picture_50_x_50()
print(f"Part 1: {hashes}")
print(f"Part 2: {ds.find_100_x_100()}")
