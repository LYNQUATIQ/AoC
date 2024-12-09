"""https://adventofcode.com/2024/day/9"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 9)


example_input = """2333133121414131402"""


def solve(inputs: str):
    i = 0
    pointer = 0
    file_id = 0
    file_sizes = {}
    file_positions = {}
    free_space = []

    disk = ""
    while True:
        file_size = int(inputs[i])
        file_sizes[file_id] = file_size
        file_positions[file_id] = pointer
        pointer += file_size
        file_id += 1
        try:
            spaces = int(inputs[i + 1])
            free_space.append(spaces)
            pointer += spaces
        except IndexError:
            break
        i += 2
    free_space.append(0)
    disk = []
    for (file_id, file_size), spaces in zip(file_sizes.items(), free_space):
        disk += ([file_id] * file_size) + ([None] * spaces)
    start_index, end_index = 0, len(disk) - 1

    check_sum = 0
    while True:
        # Find the next file block at the end
        while disk[end_index] is None:
            end_index -= 1

        # Find next free space from the start
        while disk[start_index] is not None:
            if start_index >= end_index:
                break
            check_sum += disk[start_index] * start_index
            start_index += 1

        if end_index < start_index:
            break
        check_sum += disk[end_index] * start_index
        end_index -= 1
        start_index += 1

    print(f"Part 1: {check_sum}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
# 91411296588 is too low
