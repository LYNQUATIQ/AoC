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


def tail_shift(head: XY, tail: XY) -> XY:
    x_delta, y_delta = head.x - tail.x, head.y - tail.y
    abs_x_delta, abs_y_delta = abs(x_delta), abs(y_delta)
    if abs_x_delta + abs_y_delta > 2:
        return XY(x_delta // abs_x_delta, y_delta // abs_y_delta)  # Move diagonally
    if abs_x_delta == 2:
        return XY(x_delta // abs_x_delta, 0)  # Move horizontally
    if abs_y_delta == 2:
        return XY(0, y_delta // abs_y_delta)  # Move vertically
    return XY(0, 0)  # Touching - don't move


def move_rope(number_of_knots: int, moves: list[tuple[str, int]]) -> int:
    knots = [XY(0, 0) for _ in range(number_of_knots)]
    tail_positions = {knots[-1]}
    for direction, steps in moves:
        for _ in range(steps):
            knots[0] += XY.direction(direction)
            for i in range(1, number_of_knots):
                knots[i] += tail_shift(knots[i - 1], knots[i])
            tail_positions.add(knots[-1])
    return len(tail_positions)


def solve(inputs: str) -> None:
    moves = [(d, int(n)) for d, n in [l.split() for l in inputs.splitlines()]]
    print(f"Part 1: {move_rope(2,moves)}")
    print(f"Part 2: {move_rope(10,moves)}\n")


solve(sample_input)
solve(actual_input)
