"""https://adventofcode.com/2024/day/9"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 9)


example_input = """2333133121414131402"""


def solve(inputs: str):
    i = 0
    pointer = 0
    file_id = 0
    files = {}
    free_space = {}

    disk = ""
    while True:
        files[file_id] = int(inputs[i])
        pointer += files[file_id]
        file_id += 1
        try:
            free_space[pointer] = int(inputs[i + 1])
            pointer += free_space[pointer]
        except IndexError:
            break
        i += 2
    free_space[pointer] = 0

    disk = ""
    for (file_id, file_size), spaces in zip(files.items(), free_space.values()):
        disk += str(file_id) * file_size + "." * spaces

    end_index, start_index = len(disk) - 1, 0
    sorted_disk = ""
    check_sum = 0
    file_id = 0
    while True:
        # Find next file character from the end
        while disk[end_index] == ".":
            end_index -= 1
        # Find next space character from the start
        while disk[start_index] != ".":
            if start_index >= end_index:
                break
            sorted_disk += disk[start_index]
            check_sum += int(disk[start_index]) * start_index
            start_index += 1

        if end_index < start_index:
            break
        sorted_disk += disk[end_index]
        start_index += 1
        check_sum += int(disk[end_index]) * start_index
        end_index -= 1

    print(f"Part 1: {check_sum}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
# 91411296588 is too low
