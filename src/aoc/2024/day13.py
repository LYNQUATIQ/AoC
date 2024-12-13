"""https://adventofcode.com/2024/day/13"""

import re

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 13)


example_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def solve(inputs: str):
    machine_inputs = inputs.split("\n\n")
    machines = []
    for machine_input in machine_inputs:
        button_a_line, button_b_line, prize_line = machine_input.splitlines()
        a_xy = tuple(map(int, re.findall(r"-?\d+", button_a_line)))
        b_xy = tuple(map(int, re.findall(r"-?\d+", button_b_line)))
        prize_xy = tuple(map(int, re.findall(r"-?\d+", prize_line)))
        machines.append(
            {
                "x": (a_xy[0], b_xy[0], prize_xy[0]),
                "y": (a_xy[1], b_xy[1], prize_xy[1]),
            }
        )

    total_cost = 0
    for machine in machines:
        ax, bx, prize_x = machine["x"]
        ay, by, prize_y = machine["y"]

        max_a = min(min(100, prize_x // ax), min(100, prize_y // ay))
        max_b = min(min(100, prize_x // bx), min(100, prize_y // by))

        for b in range(max_b, -1, -1):
            for a in range(max_a + 1):
                if a * ax + b * bx == prize_x and a * ay + b * by == prize_y:
                    total_cost += a * 3 + b
                    break
            else:
                continue

    print(f"Part 1: {total_cost}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
