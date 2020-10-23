import logging
import os

from grid_system import ConnectedGrid, XY


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/day_1.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/day_1_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

assert (len(lines) == 1)

directions = ((d[0], int(d[1:])) for d in lines[0].split(", "))


grid = ConnectedGrid()
xy = XY(0, 0)
facing = grid.NORTH
visited_twice = None

visited = set([xy])
for turn, steps in directions:
    if turn == "L":
        facing = grid.turn_left(facing)
    elif turn == "R":
        facing = grid.turn_right(facing)

    for _ in range(steps):
        xy += facing
        if visited_twice is None and xy in visited:
            visited_twice = xy
        visited.add(xy)

print(f"Part 1: {xy.manhattan_distance}")
print(f"Part 2: {visited_twice.manhattan_distance}")
