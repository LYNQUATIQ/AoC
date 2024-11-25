import logging
import os
import string

from grid_system import ConnectedGrid, XY


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_22.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_22_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class VirusNet(ConnectedGrid):

    UP = XY(0, -1)
    DOWN = XY(0, 1)
    RIGHT = XY(1, 0)
    LEFT = XY(-1, 0)

    left_turn = {
        UP: LEFT,
        LEFT: DOWN,
        DOWN: RIGHT,
        RIGHT: UP,
    }

    right_turn = {
        UP: RIGHT,
        RIGHT: DOWN,
        DOWN: LEFT,
        LEFT: UP,
    }

    about_turn = {
        UP: DOWN,
        DOWN: UP,
        RIGHT: LEFT,
        LEFT: RIGHT,
    }

    CLEAN = "."
    WEAKENED = "W"
    INFECTED = "#"
    FLAGGED = "F"

    def __init__(self, lines):
        super().__init__()
        top_left = -1 * (len(lines) // 2)
        y = top_left
        for line in lines:
            x = top_left
            for c in line:
                if c == self.INFECTED:
                    self.grid[XY(x, y)] = self.INFECTED
                x += 1
            y += 1
            self.current_node = XY(0, 0)
            self.current_direction = self.UP

    def do_burst(self):
        is_infected = self.grid.get(self.current_node, self.CLEAN) == self.INFECTED
        if is_infected:
            self.current_direction = self.right_turn[self.current_direction]
            self.grid[self.current_node] = self.CLEAN
        else:
            self.current_direction = self.left_turn[self.current_direction]
            self.grid[self.current_node] = self.INFECTED
        self.current_node += self.current_direction
        return not is_infected

    def do_burst2(self):
        status = self.grid.get(self.current_node, self.CLEAN)
        if status == self.CLEAN:
            self.current_direction = self.left_turn[self.current_direction]
            self.grid[self.current_node] = self.WEAKENED
        elif status == self.WEAKENED:
            self.grid[self.current_node] = self.INFECTED
        elif status == self.INFECTED:
            self.current_direction = self.right_turn[self.current_direction]
            self.grid[self.current_node] = self.FLAGGED
        elif status == self.FLAGGED:
            self.current_direction = self.about_turn[self.current_direction]
            self.grid[self.current_node] = self.CLEAN
        self.current_node += self.current_direction
        return status == self.WEAKENED


virus_net = VirusNet(lines)
become_infected = 0
for _ in range(10000):
    become_infected += virus_net.do_burst()

print(f"Part 1: {become_infected}")

virus_net = VirusNet(lines)
become_infected = 0
for _ in range(10000000):
    become_infected += virus_net.do_burst2()

print(f"Part 2: {become_infected}")
