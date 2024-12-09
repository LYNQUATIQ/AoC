"""https://adventofcode.com/2024/day/9"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 9)
example_input = """2333133121414131402"""


def solve(inputs: str):
    inputs += "0"
    pointer = 0
    file_id = 0
    file_sizes, file_positions, free_spaces = {}, {}, {}
    spaces = []
    for i in range(0, len(inputs), 2):
        file_size, space_size = int(inputs[i]), int(inputs[i + 1])
        file_sizes[file_id] = file_size
        file_positions[file_id] = pointer
        pointer += file_size
        file_id += 1
        free_spaces[pointer] = (space_size, 0)
        spaces.append(space_size)
        pointer += space_size

    disk = []
    for (file_id, file_size), n_spaces in zip(file_sizes.items(), spaces):
        disk += ([file_id] * file_size) + ([None] * n_spaces)
    start_index, end_index = 0, len(disk) - 1
    check_sum = 0
    while True:
        while disk[end_index] is None:  # Find the next file block at the end
            end_index -= 1
        while disk[start_index] is not None:  # Find next free space from the start
            if end_index < start_index:
                break
            check_sum += disk[start_index] * start_index
            start_index += 1
        if end_index < start_index:
            break
        check_sum += disk[end_index] * start_index  # Move end file block up
        end_index -= 1
        start_index += 1
    print(f"Part 1: {check_sum}")

    for file_to_move in range(len(file_positions) - 1, 0, -1):
        file_size = file_sizes[file_to_move]
        for pointer, (space, offset) in free_spaces.items():
            if pointer > file_positions[file_to_move]:
                break
            if space < file_size:
                continue
            file_positions[file_to_move] = pointer + offset
            free_spaces[pointer] = (space - file_size, offset + file_size)
            break
    check_sum = 0
    for file_id, position in file_positions.items():
        file_size = file_sizes[file_id]
        for position in range(position, position + file_size):
            check_sum += file_id * position
    print(f"Part 2: {check_sum}\n")


solve(example_input)
solve(actual_input)
