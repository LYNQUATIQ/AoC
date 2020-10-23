import logging
import os

import re

from collections import defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

regex = re.compile(r"^(?P<operation>rotate column|rect|rotate row) (?:[xy]=)*(?P<a>\d+)(?:x| by )(?P<b>\d+)$")

screen = defaultdict(int)
width = 50
height = 6

for line in lines:
    instruction = regex.match(line).groupdict()

    if instruction["operation"] == "rect":
        for x in range(int(instruction["a"])):
            for y in range(int(instruction["b"])):
                screen[(x, y)] = 1
    elif instruction["operation"] == "rotate row":
        y = int(instruction["a"])
        shift = int(instruction["b"])
        row = [screen[(x, y)] for x in range(width)]
        for x in range(width):
            screen[(x, y)] = row[(x - shift) % width]
    elif instruction["operation"] == "rotate column":
        x = int(instruction["a"])
        shift = int(instruction["b"])
        column = [screen[(x, y)] for y in range(height)]
        for y in range(height):
            screen[(x, y)] = column[(y - shift) % height]       

print(f"Part 1: {sum(screen.values())}")
print(f"Part 2:")
for y in range(height):
    for x in range(width):
        print({1:u"\u2588", 0:" "}[screen[(x, y)]], end="")
    print()
print()