"""https://adventofcode.com/2024/day/13"""

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


def find_total_cost(
    machines: list[tuple[int, int, int, int, int, int]], extra_distance: int = 0
):
    """See https://en.wikipedia.org/wiki/Diophantine_equation

    Assuming A,B are the number of times we press the buttons A and B, then:
        ax * A  +  bx * B  =  prize_x
        ay * A  +  by * B  =  prize_y

    Find the lcm of ax,ay and then multiply through by lcm/ax and -lcm/ay so that:
       lcm * A  + bx' * B  =  prize_x'
      -lcm * A  + by' * B  =  prize_y'

    Add the equations together to give a single equation with one unknown, B.
    Rearrange to find B, and then A (checking they're integers, i.e. a solution exists)
        B = (prize_x' + prize_y') / (bx' + by')
        A = (prize_x' - B * bx') / ax
    """
    total_cost = 0
    for ax, ay, bx, by, prize_x, prize_y in machines:
        prize_x += extra_distance
        prize_y += extra_distance

        lcm = math.lcm(ax, ay)
        ax, bx, prize_x = ax * (lcm / ax), bx * (lcm / ax), prize_x * (lcm / ax)
        ay, by, prize_y = ay * (-lcm / ay), by * (-lcm / ay), prize_y * (-lcm / ay)

        b_presses = (prize_x + prize_y) / (bx + by)
        a_presses = (prize_x - b_presses * bx) / ax

        if b_presses == int(b_presses) and a_presses == int(a_presses):
            total_cost += int(a_presses * 3 + b_presses)

    return total_cost


def solve(inputs: str):
    machines = [tuple(map(int, re.findall(r"\d+", m))) for m in inputs.split("\n\n")]
    print(f"Part 1: {find_total_cost(machines)}")
    print(f"Part 2: {find_total_cost(machines, 10_000_000_000_000)}\n")


solve(example_input)
solve(actual_input)
