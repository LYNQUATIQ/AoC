import os
from intcode_computer import IntCodeComputer
from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]

WHITE = 1
BLACK = 0


def paint_hull(starting_panel_color):
    painted = set()
    xy = XY(0, 0)
    direction = ConnectedGrid.NORTH
    hull = ConnectedGrid()
    hull.grid[xy] = starting_panel_color
    computer = IntCodeComputer(program)
    while not computer.is_terminated():
        computer.run_program([hull.grid.get(xy, BLACK)])
        color, turn = computer.output()[-2:]
        if color:
            painted.add(xy)
        hull.grid[xy] = color
        direction = {0: hull.turn_left, 1: hull.turn_right}[turn](direction)
        xy += direction
    return painted, hull


painted, _ = paint_hull(BLACK)
print(f"Part 1: {len(painted)}")

_, grid = paint_hull(WHITE)
print("Part 2:")
grid.print_grid({WHITE: "\u2588", BLACK: " "})
