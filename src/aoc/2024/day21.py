"""https://adventofcode.com/2024/day/21"""

from collections import deque

from aoc_utils import get_input_data, print_time_taken

actual_input = get_input_data(2024, 21)
example_input = """029A
980A
179A
456A
379A"""

UP, DOWN, LEFT, RIGHT, ACTIVATE = "^", "v", "<", ">", "A"
NUMERIC_KEYPAD = {
    "0": {UP: "2", RIGHT: "A", DOWN: None, LEFT: None},
    "1": {UP: "4", RIGHT: "2", DOWN: None, LEFT: None},
    "2": {UP: "5", RIGHT: "3", DOWN: "0", LEFT: "1"},
    "3": {UP: "6", RIGHT: None, DOWN: "A", LEFT: "2"},
    "4": {UP: "7", RIGHT: "5", DOWN: "1", LEFT: None},
    "5": {UP: "8", RIGHT: "6", DOWN: "2", LEFT: "4"},
    "6": {UP: "9", RIGHT: None, DOWN: "3", LEFT: "5"},
    "7": {UP: None, RIGHT: "8", DOWN: "4", LEFT: None},
    "8": {UP: None, RIGHT: "9", DOWN: "5", LEFT: "7"},
    "9": {UP: None, RIGHT: None, DOWN: "6", LEFT: "8"},
    "A": {UP: "3", RIGHT: None, DOWN: None, LEFT: "0"},
}

DIRECTIONAL_KEYPAD = {
    UP: {DOWN: DOWN, RIGHT: ACTIVATE, UP: None, LEFT: None},
    DOWN: {DOWN: None, RIGHT: RIGHT, UP: UP, LEFT: LEFT},
    LEFT: {DOWN: None, RIGHT: DOWN, UP: None, LEFT: None},
    RIGHT: {DOWN: None, RIGHT: None, UP: ACTIVATE, LEFT: DOWN},
    ACTIVATE: {DOWN: RIGHT, RIGHT: None, UP: None, LEFT: UP},
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
    return paths


def all_paths(keypad):
    return {(k0, k1): paths(k0, k1, keypad) for k1 in keypad for k0 in keypad}


NUMERIC_PATHS = all_paths(NUMERIC_KEYPAD)
DIRECTIONAL_PATHS = all_paths(DIRECTIONAL_KEYPAD)


def numeric_sequences(code):
    if code == ACTIVATE:
        return [""]
    sequences = []
    next_steps = NUMERIC_PATHS[(code[0], code[1])]
    remaining = numeric_sequences(code[1:])
    for next_step in next_steps:
        for remainder in remaining:
            sequences.append(next_step + ACTIVATE + remainder)
    return sequences


def directional_sequences(instructions):
    if instructions == ACTIVATE:
        return [""]
    sequences = []
    next_steps = DIRECTIONAL_PATHS[(instructions[0], instructions[1])]
    remaining = directional_sequences(instructions[1:])
    for next_step in next_steps:
        for remainder in remaining:
            sequences.append(next_step + ACTIVATE + remainder)
    return sequences


def shortest_sequence(code):
    keypad_sequences = numeric_sequences("A" + code)
    robot_sequences = []
    for keypad_sequence in keypad_sequences:
        robot_sequences += directional_sequences("A" + keypad_sequence)
    final_sequences = []
    for robot_sequence in robot_sequences:
        final_sequences += directional_sequences("A" + robot_sequence)
    return min(final_sequences, key=len)


@print_time_taken
def solve(inputs: str):
    codes = inputs.splitlines()
    total_complexity = 0

    for code in codes:
        numeric_part = int(code[:-1])
        sequence = shortest_sequence(code)
        total_complexity += len(sequence) * numeric_part

    print(f"Part 1: {total_complexity}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
