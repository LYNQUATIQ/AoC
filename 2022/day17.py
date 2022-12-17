"""https://adventofcode.com/2022/day/17"""
import os

from itertools import cycle

with open(os.path.join(os.path.dirname(__file__), f"inputs/day17_input.txt")) as f:
    actual_input = f.read()


sample_input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

# Coords give shape pixels relative to bottom left of shape
# ━ ╋ ┛ ┃ ■
SHAPES = (
    (0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j),
    (1 + 0j, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j),
    (0 + 0j, 1 + 0j, 2 + 0j, 2 + 1j, 2 + 2j),
    (0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j),
    (0 + 0j, 1 + 0j, 0 + 1j, 1 + 1j),
)

SHAPE_HEIGHTS = (1, 3, 3, 4, 2)
SHAPE_WIDTHS = (4, 3, 3, 1, 2)

# Coords give spaces required (relative to bottom left of shape) to move DOWN
# ━ ╋ ┛ ┃ ■
SPACE_DOWN = (
    (0 - 1j, 1 - 1j, 2 - 1j, 3 - 1j),
    (0 + 0j, 1 - 1j, 2 + 0j),
    (0 - 1j, 1 - 1j, 2 - 1j),
    (0 - 1j,),
    (0 - 1j, 1 - 1j),
)

# Coords give spaces required (relative to bottom left of shape) to move LEFT
# ━ ╋ ┛ ┃ ■
SPACE_LEFT = (
    (-1 + 0j,),
    (0 + 0j, -1 + 1j, 0 + 2j),
    (-1 + 0j, 1 + 1j, 1 + 2j),
    (-1 + 0j, -1 + 1j, -1 + 2j, -1 + 3j),
    (-1 + 0j, -1 + 1j),
)

# Coords give spaces required (relative to bottom left of shape) to move RIGHT
# ━ ╋ ┛ ┃ ■
SPACE_RIGHT = (
    (4 + 0j,),
    (2 + 0j, 3 + 1j, 2 + 2j),
    (3 + 0j, 3 + 1j, 3 + 2j),
    (1 + 0j, 1 + 1j, 1 + 2j, 1 + 3j),
    (2 + 0j, 2 + 1j),
)

SPACES_TO_CHECK = {"<": (SPACE_LEFT, -1 + 0j), ">": (SPACE_RIGHT, 1 + 0j)}


class Chamber:
    def __init__(self) -> None:
        self._rocks: set[complex] = set()

    def add_rock(self, xy: complex) -> None:
        assert xy not in self._rocks
        self._rocks.add(xy)

    def blocked(self, xy: complex) -> bool:
        if xy.real < 0 or xy.real >= 7 or xy.imag <= 0:
            return True
        return xy in self._rocks

    def __repr__(self) -> str:
        output = ""
        height = max(int(xy.imag) for xy in self._rocks)
        for y in range(height, 0, -1):
            output += "|"
            for x in range(7):
                output += "#" if complex(x, y) in self._rocks else "."
            output += f"| {y}\n"
        output += "+-------+ 0\n"

        return output


def play_tetris(puffs: str, iterations: int) -> int:
    puff_cycle = cycle(puffs)
    shape_cycle = cycle(range(5))
    chamber = Chamber()
    max_height = 0
    for i in range(iterations):
        shape = next(shape_cycle)
        position = complex(2, max_height + 4)
        stopped = False
        while not stopped:
            # Try to move left/right
            puff = next(puff_cycle)
            space_requirements, offset = SPACES_TO_CHECK[puff]
            spaces_to_check = space_requirements[shape]
            if not any(chamber.blocked(position + d) for d in spaces_to_check):
                position += offset

            # Try to move down
            spaces_to_check = SPACE_DOWN[shape]
            stopped = any(chamber.blocked(position + d) for d in spaces_to_check)
            if not stopped:
                position += 0 - 1j

        for rock in SHAPES[shape]:
            chamber.add_rock(position + rock)
        max_height = max(max_height, int(position.imag) + SHAPE_HEIGHTS[shape] - 1)

    return max_height


def solve(inputs: str) -> None:
    print(f"Part 1: {play_tetris(inputs, 2022)}")
    # print(f"Part 2: {play_tetris(inputs, 1_000_000_000_000)}\n")


solve(sample_input)
solve(actual_input)
