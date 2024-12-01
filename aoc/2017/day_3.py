import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_3.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

puzzle_input = 368078

grid = {}
x, y = 0, 0
i = 1
grid = {i: (x, y)}
current_spiral = 0
while i < puzzle_input:
    current_spiral += 1
    x += 1
    y -= 1
    side_length = current_spiral * 2
    for direction in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
        xd, yd = direction
        for _ in range(side_length):
            x += xd
            y += yd
            i += 1
            grid[i] = (x, y)

x, y = grid[puzzle_input]
print(f"Part 1: {abs(x) + abs(y)}")


def calculate_part_2():
    grid = defaultdict(int)
    x, y = 0, 0
    grid[(x, y)] = 1
    current_spiral = 0
    while True:
        current_spiral += 1
        x += 1
        y -= 1
        side_length = current_spiral * 2
        for direction in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            xd, yd = direction
            for _ in range(side_length):
                x += xd
                y += yd
                total_neighbours = sum(
                    [
                        grid[(x - 1, y - 1)],
                        grid[(x + 0, y - 1)],
                        grid[(x + 1, y - 1)],
                        grid[(x - 1, y + 0)],
                        grid[(x + 1, y + 0)],
                        grid[(x - 1, y + 1)],
                        grid[(x + 0, y + 1)],
                        grid[(x + 1, y + 1)],
                    ]
                )
                grid[(x, y)] = total_neighbours
                if total_neighbours > puzzle_input:
                    return total_neighbours


print(f"Part 2: {calculate_part_2()}")
