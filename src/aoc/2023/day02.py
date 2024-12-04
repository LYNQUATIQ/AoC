"""https://adventofcode.com/2023/day/2"""

import os
import math
import re

with open(os.path.join(os.path.dirname(__file__), "inputs/day02_input.txt")) as f:
    actual_input = f.read()


example_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

RED, GREEN, BLUE = "red", "green", "blue"
MAX_COUNT = {RED: 12, GREEN: 13, BLUE: 14}


def solve(inputs: str):
    total = 0
    total_power = 0
    for game in inputs.splitlines():
        game_id = int(re.search(r"\d+", game).group())
        cube_count = {
            colour: max(map(int, re.findall(rf"(\d+) {colour}", game)))
            for colour in [RED, GREEN, BLUE]
        }
        if all(cube_count[c] <= MAX_COUNT[c] for c in cube_count):
            total += game_id
        total_power += math.prod(cube_count.values())

    print(f"Part 1: {total}")
    print(f"Part 2: {total_power}\n")


solve(example_input)
solve(actual_input)
