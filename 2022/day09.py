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

# fmt:off
TAIL_MOVE = {
    -2-2j: -1-1j, -2-1j: -1-1j, -1-2j: -1-1j,  # Above and to the left
    2-2j: 1-1j, 1-2j: 1-1j, 2-1j: 1-1j,        # Above and to the right
    -2+2j: -1+1j, -2+1j :-1+1j, -1+2j: -1+1j,  # Below and to the left
    2+2j: 1+1j, 1+2j: 1+1j, 2+1j: 1+1j,        # Below and to the right
    -2j: -1j, 2j: 1j, -2: -1, 2: 1,            # Above, below, left or right
}
# fmt:on


def solve(inputs: str) -> None:
    knots = [0 + 0j] * 10
    visited = [{knot} for knot in knots]
    for direction, distance in [move.split() for move in inputs.splitlines()]:
        for _ in range(int(distance)):
            knots[0] += {"L": -1, "R": 1, "U": -1j, "D": 1j}[direction]  # Move head
            for i in range(1, len(knots)):
                knots[i] += TAIL_MOVE.get(knots[i - 1] - knots[i], 0)  # Move tails
                visited[i].add(knots[i])

    print(f"Part 1: {len(visited[1])}")
    print(f"Part 2: {len(visited[9])}\n")


solve(sample_input)
solve(actual_input)
