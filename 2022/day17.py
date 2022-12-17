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


State = tuple


def play_tetris(puffs: str, number_of_rocks: int) -> int:
    puff_cycle, puff_index = len(puffs), 0
    shape_cycle = cycle(range(5))

    # Chamber always has seven blank rows for shape to start in
    chamber = bytearray([0] * 7 + [0b11111111])
    prior_states: dict[State, int] = {}
    prior_heights: dict[int, int] = {0: 0}

    rocks, current_height = 0, 0
    while True:

        shape_id = next(shape_cycle)
        shape = list(SHAPES[shape_id])
        rocks += 1
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

        current_height += 7 - min(i, 7)
        new_chamber = bytearray([0] * 7) + chamber[min(i, 7) :]
        chamber = new_chamber

        state = (tuple(chamber[:20]), shape_id, puff_index)
        if state in prior_states:
            prior_rocks = prior_states[state]
            prior_height = prior_heights[prior_rocks]
            height_change = current_height - prior_height
            cycle_length = rocks - prior_rocks
            remaining_rocks = number_of_rocks - prior_rocks
            number_of_cycles = remaining_rocks // cycle_length
            remaining_rocks = remaining_rocks % cycle_length
            total_height = prior_height
            total_height += number_of_cycles * height_change
            total_height += prior_heights[remaining_rocks + prior_rocks] - prior_height
            return total_height
        else:
            prior_states[state] = rocks
        prior_heights[rocks] = current_height

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
