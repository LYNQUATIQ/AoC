"""https://adventofcode.com/2022/day/9"""
import os

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

TAIL_MOVE = {
    (-2, -2): (-1, -1),
    (-2, -1): (-1, -1),
    (-2, 0): (-1, 0),
    (-2, 1): (-1, 1),
    (-2, 2): (-1, 1),
    (-1, -2): (-1, -1),
    (-1, 2): (-1, 1),
    (0, -2): (0, -1),
    (0, 2): (0, 1),
    (1, -2): (1, -1),
    (1, 2): (1, 1),
    (2, -2): (1, -1),
    (2, -1): (1, -1),
    (2, 0): (1, 0),
    (2, 1): (1, 1),
    (2, 2): (1, 1),
}


def move_rope(number_of_knots: int, moves: list[tuple[str, int]]) -> int:
    knots = [[0, 0] for _ in range(number_of_knots)]
    head, tail = knots[0], knots[-1]
    tail_positions = {tuple(tail)}
    for direction, steps in moves:
        for _ in range(steps):
            head[0] += {"L": -1, "R": 1}.get(direction, 0)
            head[1] += {"U": -1, "D": 1}.get(direction, 0)
            for h, t in zip(knots[:-1], knots[1:]):
                dx, dy = TAIL_MOVE.get((h[0] - t[0], h[1] - t[1]), (0, 0))
                t[0], t[1] = t[0] + dx, t[1] + dy
            tail_positions.add(tuple(tail))
    return len(tail_positions)


def solve(inputs: str) -> None:
    moves = [(d, int(n)) for d, n in [l.split() for l in inputs.splitlines()]]
    print(f"Part 1: {move_rope(2,moves)}")
    print(f"Part 2: {move_rope(10,moves)}\n")


solve(sample_input)
solve(actual_input)
