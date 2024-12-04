"""https://adventofcode.com/2021/day/2"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day02_input.txt")) as f:
    actual_input = f.read()

example_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def solve(input_txt):
    position, depth, aim = 0, 0, 0
    for line in input_txt.splitlines():
        match line.split():
            case ("forward", x):
                position += int(x)
                depth += aim * int(x)
            case ("up", x):
                aim -= int(x)
            case ("down", x):
                aim += int(x)

    print(f"Part 1: {position * aim}")
    print(f"Part 2: {position * depth}\n")


solve(example_input)
solve(actual_input)
