"""https://adventofcode.com/2022/day/17"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day17_input.txt")) as f:
    actual_input = f.read()


sample_input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

SHAPES = (
    (0b00111100,),  # ━
    (0b00010000, 0b00111000, 0b00010000),  # ╋
    (0b00001000, 0b00001000, 0b00111000),  # ┛
    (0b00100000, 0b00100000, 0b00100000, 0b00100000),  # ┃
    (0b00110000, 0b00110000),  # ■
)


def play_tetris(puffs: str, number_of_rocks: int) -> int:
    puff_cycle, puff_index = len(puffs), 0
    shape_cycle, shape_index = len(SHAPES), 0

    # Chamber has seven blank rows for shape to start in - row 3 plus 4 for shape itself
    chamber = bytearray([0] * 7 + [0b11111111])

    prior_states: dict[tuple[tuple[int, ...], int, int], int] = {}
    prior_heights: dict[int, int] = {0: 0}

    rocks, current_height = 0, 0
    while True:
        rocks += 1
        shape = list(SHAPES[shape_index])
        shape_index = (shape_index + 1) % shape_cycle
        
        i = 4 - len(shape)
        while True:
            
            # Try moving left/right making sure we don't move into an edge
            puff = puffs[puff_index]
            puff_index = (puff_index + 1) % puff_cycle
            match puff:
                case '>': shifted, edge = [x // 2 for x in shape], 1
                case '<': shifted, edge = [x * 2 for x in shape], 256
            if not any((s & edge) or (s & c) for s, c in zip(shifted, chamber[i:])):
                shape = shifted
                
            # Try moving down - break out if we hit any rocks in the cavern
            if any((s & c) for s, c in zip(shape, chamber[i + 1 :])):
                break
            i += 1

        # Fix shape in chamber
        for chamber_index, shape_row in enumerate(shape, start=i):
            chamber[chamber_index] |= shape_row

        current_height += 7 - min(i, 7)
        chamber = bytearray([0] * 7) + chamber[min(i, 7) :]
        state = (tuple(chamber[:20]), shape_index, puff_index)
        if state in prior_states:
            prior_rocks = prior_states[state]
            prior_height = prior_heights[prior_rocks]
            cycle_length = rocks - prior_rocks
            remaining_rocks = number_of_rocks - prior_rocks
            number_of_cycles = remaining_rocks // cycle_length
            remaining_rocks = remaining_rocks % cycle_length
            total_height = prior_height
            total_height += number_of_cycles * (current_height - prior_height)
            total_height += prior_heights[remaining_rocks + prior_rocks] - prior_height
            return total_height

        prior_states[state] = rocks
        prior_heights[rocks] = current_height


def solve(inputs: str) -> None:
    print(f"Part 1: {play_tetris(inputs, 2022)}")
    print(f"Part 2: {play_tetris(inputs, 1_000_000_000_000)}\n")


solve(sample_input)
solve(actual_input)
