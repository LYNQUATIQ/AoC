import logging
import os

import string

from collections import defaultdict
from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

snakes = ConnectedGrid()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        snakes.grid[XY(x, y)] = c


def possible_directions(xy):
    return [
        d for d in snakes.DIRECTIONS if snakes.grid[xy + d] in string.ascii_lowercase
    ]


_, _, max_x, max_y = snakes.get_limits()
snake_heads = {}
for x in range(max_x):
    for y in range(max_y):
        xy = XY(x, y)
        if snakes.grid[xy] in string.ascii_lowercase:
            directions = possible_directions(xy)
            if len(directions) == 1:
                snake_heads[xy] = directions[0]

all_snakes = {}
snakes_to_traverse = list(snake_heads.keys())
while snakes_to_traverse:
    head = snakes_to_traverse[0]
    direction = snake_heads[head]
    xy = head
    words = []
    word = ""
    while direction:
        while snakes.grid[xy] in string.ascii_lowercase:
            word += snakes.grid[xy]
            xy += direction
        xy -= direction
        words.append(word)
        word = ""
        directions = possible_directions(xy)
        if len(directions) == 2:
            r = snakes.turn_right(direction)
            l = snakes.turn_left(direction)
            if r in directions:
                direction = r
            else:
                direction = snakes.turn_left(direction)
        else:
            direction = None
    all_snakes[head] = words
    snakes_to_traverse.remove(head)
    snakes_to_traverse.remove(xy)

print(all_snakes)


def word_value(word):
    letter_values = {c: v for v, c in enumerate(string.ascii_lowercase, 1)}
    return sum(list(map(letter_values.get, word))) * len(word)


answer = 0
for snake in all_snakes.values():
    for word in snake:
        answer += word_value(word)

print(answer)
