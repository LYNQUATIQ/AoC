import os

from grid import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """F10
N3
F7
R90
F11"""


class NavigationSystem:
    def __init__(self, waypoint, move_waypoint):
        self.ship = XY(0, 0)
        self.waypoint = waypoint
        self.move_waypoint = move_waypoint

    def follow_instructions(self, instructions):
        for instruction, steps in instructions:
            if instruction in "LR":
                steps = (360 - steps) // 90 if instruction == "R" else steps // 90
            for _ in range(steps):
                if instruction in "NEWS":
                    if self.move_waypoint:
                        self.waypoint += XY.direction(instruction)
                    else:
                        self.ship += XY.direction(instruction)
                elif instruction in "LR":
                    self.waypoint = XY(self.waypoint.y, -self.waypoint.x)
                else:
                    self.ship += self.waypoint
        return self.ship.manhattan_distance


def solve(inputs):
    instructions = [(line[0], int(line[1:])) for line in inputs.split("\n")]

    part1 = NavigationSystem(XY(1, 0), False).follow_instructions(instructions)
    print(f"Part 2: {part1}")
    part2 = NavigationSystem(XY(10, -1), True).follow_instructions(instructions)
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
