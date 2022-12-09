"""https://adventofcode.com/2022/day/9"""
import os

from grid import XY

with open(os.path.join(os.path.dirname(__file__), f"inputs/day09_input.txt")) as f:
    actual_input = f.read()


sample_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def move_knot(head: XY, tail: XY) -> XY:
    x_delta, y_delta = head.x - tail.x, head.y - tail.y
    x_shift, y_shift = 0, 0
    if abs(x_delta) == 2:
        x_shift = x_delta // 2
        y_shift = y_delta
    elif abs(y_delta) == 2:
        x_shift = x_delta
        y_shift = y_delta // 2
    if abs(x_delta) == 2 and abs(y_delta) == 2:
        x_shift = x_delta // 2
        y_shift = y_delta // 2
    return XY(x_shift, y_shift)


def move_rope(number_of_knots: int, motions) -> int:
    knots = [XY(0, 0) for _ in range(number_of_knots)]
    tail_positions = {knots[-1]}
    for direction, steps in motions:
        for _ in range(steps):
            knots[0] += XY.direction(direction)
            for i in range(1, number_of_knots):
                shift = move_knot(knots[i - 1], knots[i])
                knots[i] += shift
            tail_positions.add(knots[-1])
    return len(tail_positions)


def solve(inputs: str) -> None:
    motions = []
    for line in inputs.splitlines():
        a, b = line.split()
        motions.append((a, int(b)))

    print(f"Part 1: {move_rope(2,motions)}")
    print(f"Part 2: {move_rope(10,motions)}\n")


solve(sample_input)
solve(actual_input)
