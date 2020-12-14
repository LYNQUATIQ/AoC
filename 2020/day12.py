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


def navigate_ship(instructions, waypoint, move_waypoint):
    ship = XY(0, 0)
    for instruction, steps in instructions:
        if instruction in "LR":
            steps = (360 - steps) // 90 if instruction == "R" else steps // 90
        for _ in range(steps):
            if instruction in "NSEW":
                if move_waypoint:
                    waypoint += XY.direction(instruction)
                else:
                    ship += XY.direction(instruction)
            elif instruction in "LR":
                waypoint = XY(waypoint.y, -waypoint.x)
            else:
                ship += waypoint
    return ship.manhattan_distance


def solve(inputs):
    instructions = [(line[0], int(line[1:])) for line in inputs.split("\n")]
    print(f"Part 2: {navigate_ship(instructions, XY(1, 0), False)}")
    print(f"Part 2: {navigate_ship(instructions, XY(10, -1), True)}\n")


solve(sample_input)
solve(actual_input)
