"""https://adventofcode.com/2024/day/21"""

from collections import deque
from functools import cache

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 21)
example_input = """029A
980A
179A
456A
379A"""

UP, DOWN, LEFT, RIGHT, ACTIVATE = "^", "v", "<", ">", "A"
NUMERIC_KEYPAD = {
    "0": {UP: "2", RIGHT: "A"},
    "1": {UP: "4", RIGHT: "2"},
    "2": {UP: "5", RIGHT: "3", DOWN: "0", LEFT: "1"},
    "3": {UP: "6", DOWN: "A", LEFT: "2"},
    "4": {UP: "7", RIGHT: "5", DOWN: "1"},
    "5": {UP: "8", RIGHT: "6", DOWN: "2", LEFT: "4"},
    "6": {UP: "9", DOWN: "3", LEFT: "5"},
    "7": {RIGHT: "8", DOWN: "4"},
    "8": {RIGHT: "9", DOWN: "5", LEFT: "7"},
    "9": {DOWN: "6", LEFT: "8"},
    "A": {UP: "3", LEFT: "0"},
}
DIRECTIONAL_KEYPAD = {
    UP: {DOWN: DOWN, RIGHT: ACTIVATE},
    DOWN: {RIGHT: RIGHT, UP: UP, LEFT: LEFT},
    LEFT: {RIGHT: DOWN},
    RIGHT: {UP: ACTIVATE, LEFT: DOWN},
    ACTIVATE: {DOWN: RIGHT, LEFT: UP},
}


def paths(start_key: str, target_key: str, keypad: dict[str, dict[str, str]]) -> str:
    paths = []
    to_visit = deque([(start_key, "")])
    while to_visit:
        current_key, sequence = to_visit.popleft()
        if paths and len(sequence) > len(paths[0]):
            break
        if current_key == target_key:
            paths.append(sequence)
        for direction, next_key in keypad[current_key].items():
            if next_key is not None:
                to_visit.append((next_key, sequence + direction))
    return tuple(paths)


def all_paths(keypad):
    return {(k0, k1): paths(k0, k1, keypad) for k1 in keypad for k0 in keypad}


NUMERIC_PATHS = all_paths(NUMERIC_KEYPAD)
DIRECTIONAL_PATHS = all_paths(DIRECTIONAL_KEYPAD)


@cache
def best_sequence(instructions, directional_robots):
    if directional_robots == 0:
        return len(instructions) + 1
    sequence = 0
    for instruction_pair in zip("A" + instructions, instructions + ACTIVATE):
        sequences = []
        paths = DIRECTIONAL_PATHS[instruction_pair]
        for path in paths:
            sequences.append(best_sequence(path, directional_robots - 1))
        sequence += min(sequences)

    return sequence


def best_code_sequence(code, directional_robots):
    sequence = 0
    for numeric_pair in zip("A" + code[:-1], code):
        sequences = []
        paths = NUMERIC_PATHS[numeric_pair]
        for path in paths:
            sequences.append(best_sequence(path, directional_robots))
        sequence += min(sequences)
    return sequence


def total_complexity(codes, directional_robots):
    total_complexity = 0
    for code in codes:
        numeric_part = int(code[:-1])
        shortest_sequence = best_code_sequence(code, directional_robots)
        total_complexity += shortest_sequence * numeric_part

    return total_complexity


def solve(inputs: str):
    codes = inputs.splitlines()

    print(f"Part 1: {total_complexity(codes, directional_robots=2)}")
    print(f"Part 2: {total_complexity(codes, directional_robots=25)}\n")


solve(example_input)
solve(actual_input)
