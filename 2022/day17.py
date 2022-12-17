"""https://adventofcode.com/2022/day/17"""
import os

from itertools import cycle

with open(os.path.join(os.path.dirname(__file__), f"inputs/day17_input.txt")) as f:
    actual_input = f.read()


sample_input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

SHAPES = (
    (0b00111100,),  # ━
    (
        0b00010000,  # ╋
        0b00111000,
        0b00010000,
    ),
    (
        0b00001000,  # ┛
        0b00001000,
        0b00111000,
    ),
    (
        0b00100000,  # ┃
        0b00100000,
        0b00100000,
        0b00100000,
    ),
    (
        0b00110000,  # ■
        0b00110000,
    ),
)


class Chamber:
    def __init__(self) -> None:
        self._rocks: set[complex] = set()
        self._last_rock: set[complex] = set()

    def add_rock(self, xy: complex) -> None:
        assert xy not in self._rocks
        self._rocks.add(xy)

    def add_rocks(self, position: complex, shape: tuple[complex, ...]) -> None:
        self._last_rock = set(position + xy for xy in shape)
        for xy in self._last_rock:
            self.add_rock(xy)

    def blocked(self, xy: complex) -> bool:
        if xy.real < 0 or xy.real >= 7 or xy.imag <= 0:
            return True
        return xy in self._rocks

    def __repr__(self) -> str:
        output = ""
        height = max(int(xy.imag) for xy in self._rocks)
        for y in range(height + 3, max(height - 20, 0), -1):
            output += "|"
            for x in range(7):
                c = "#" if complex(x, y) in self._rocks else "."
                c = "@" if complex(x, y) in self._last_rock else c
                output += c
            output += f"| {y}\n"
        if y == 1:
            output += "+-------+ 0\n"

        return output


State = tuple

CHAMBER_LENGTH = 36


def play_tetris(puffs: str, number_of_rocks: int) -> int:
    puff_cycle, puff_index = len(puffs), 0
    shape_cycle = cycle(range(5))

    # Chamber always has seven blank rows for shape to start in and a minimum of 36 rows
    chamber = bytearray([0] * 7 + [0b11111111] * CHAMBER_LENGTH)
    prior_states: dict[State, int] = {}
    prior_heights: dict[int, int] = {0: 0}
    current_height = 0
    max_drop = 0
    for iteration in range(number_of_rocks):
        shape_id = next(shape_cycle)
        shape = list(SHAPES[shape_id])
        i = 4 - len(shape)
        while True:

            # Try to move left/right
            puff = puffs[puff_index]
            puff_index = (puff_index + 1) % puff_cycle

            if puff == ">":
                new_shape = [x // 2 for x in shape]
                if not any((s & 1) or (s & c) for s, c in zip(new_shape, chamber[i:])):
                    if new_shape == [1, 1, 1, 1]:
                        breakpoint()
                    shape = new_shape
            else:
                new_shape = [x * 2 for x in shape]
                if not any(
                    (s & 256) or (s & c) for s, c in zip(new_shape, chamber[i:])
                ):
                    shape = new_shape

            # Try to move down
            if any((s & c) for s, c in zip(shape, chamber[i + 1 :])):
                break
            i += 1
        for c, s in enumerate(shape, start=i):
            chamber[c] |= s

        max_drop = max(max_drop, i)
        current_height += 7 - min(i, 7)
        new_chamber = bytearray([0] * 7) + chamber[min(i, 7) :]
        chamber = new_chamber

        rocks_so_far = iteration + 1
        # print(f"Rocks:  {rocks_so_far}\nHeight: {current_height}")
        # print_chamber(chamber, current_height)
        # # input()

        state = (tuple(chamber[:CHAMBER_LENGTH]), shape_id, puff_index)
        if state in prior_states:
            prior_rocks = prior_states[state]
            prior_height = prior_heights[prior_rocks]
            height_change = current_height - prior_height
            cycle_length = rocks_so_far - prior_rocks
            remaining_rocks = number_of_rocks - prior_rocks
            number_of_cycles = remaining_rocks // cycle_length
            remaining_rocks = remaining_rocks % cycle_length
            total_height = prior_height
            total_height += number_of_cycles * height_change
            total_height += prior_heights[remaining_rocks + prior_rocks] - prior_height
            return total_height
        else:
            prior_states[state] = rocks_so_far
        prior_heights[rocks_so_far] = current_height

    raise ValueError


def print_chamber(chamber: bytearray, height: int) -> None:
    for y, c in enumerate(chamber[:24]):
        row = "".join("#" if c & (2 ** n) else "." for n in range(7, 0, -1))
        print("|" + row + "|", f"height = {height}" if y == 7 else "")


def solve(inputs: str) -> None:
    print(f"Part 1: {play_tetris(inputs, 2022)}")
    print(f"Part 2: {play_tetris(inputs, 1_000_000_000_000)}\n")


# 1528323699449 <- too high

solve(sample_input)
solve(actual_input)
