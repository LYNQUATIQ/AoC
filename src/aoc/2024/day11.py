"""https://adventofcode.com/2024/day/11"""

from functools import cache

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 11)
example_input = "125 17"


@cache
def stone_count(stone_value: int, iterations_to_do: int) -> int:
    if iterations_to_do == 0:
        return 1

    # Determine the stone(s) after we iterate (i.e. blink at) this stone
    if stone_value == 0:
        stones_after_iteration = [1]
    elif len(str(stone_value)) % 2 == 0:
        stones_after_iteration = [
            int(str(stone_value)[: len(str(stone_value)) // 2]),
            int(str(stone_value)[len(str(stone_value)) // 2 :]),
        ]
    else:
        stones_after_iteration = [stone_value * 2024]

    return total_stone_count(stones_after_iteration, iterations_to_do - 1)


def total_stone_count(stones: list[int], iterations_to_do: int) -> int:
    return sum(stone_count(stone, iterations_to_do) for stone in stones)


def solve(inputs: str):
    inital_stones = list(map(int, inputs.split()))
    print(f"Part 1: {total_stone_count(inital_stones, 25)}")
    print(f"Part 2: {total_stone_count(inital_stones, 75)}\n")


solve(example_input)
solve(actual_input)
