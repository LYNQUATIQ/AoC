"""https://adventofcode.com/2024/day/13
    https://en.wikipedia.org/wiki/Diophantine_equation
"""

import math
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


def find_total_cost(machines: dict, extra_distance: int = 0):
    total_cost = 0
    for machine in machines:

        ax, bx, prize_x = machine["x"]
        ay, by, prize_y = machine["y"]
        prize_x += extra_distance
        prize_y += extra_distance

        # Find the lcm of ax and bx
        lcm = math.lcm(ax, ay)
        ax, bx, prize_x = ax * (lcm // ax), bx * (lcm // ax), prize_x * (lcm // ax)
        ay, by, prize_y = ay * (-lcm // ay), by * (-lcm // ay), prize_y * (-lcm // ay)

        b_presses = (prize_x + prize_y) / (by + bx)
        a_presses = (prize_x - b_presses * bx) / ax
        if b_presses != int(b_presses) or a_presses != int(a_presses):
            continue
        total_cost += int(a_presses * 3 + b_presses)

    return total_cost


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

    print(f"Part 1: {find_total_cost(machines)}")
    print(f"Part 2: {find_total_cost(machines, 10_000_000_000_000)}\n")


solve(example_input)
solve(actual_input)
