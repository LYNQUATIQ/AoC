"""https://adventofcode.com/2024/day/11"""

from collections import defaultdict
from email.policy import default
from functools import cache

actual_input = "9694820 93 54276 1304 314 664481 0 4"
example_input = "125 17"

stone_count_cache = defaultdict(dict)


@cache
def process_value(value: int) -> list[int]:
    if value == 0:
        return [1]
    if len(str(value)) % 2 == 0:
        lhs = int(str(value)[: len(str(value)) // 2])
        rhs = int(str(value)[len(str(value)) // 2 :])
        return [lhs, rhs]
    return [value * 2024]


def stone_count(stone_value: int, iterations_left: int) -> int:
    if iterations_left == 0:
        return 1
    try:
        return stone_count_cache[stone_value][iterations_left]
    except KeyError:
        pass

    total_stones = 0
    for value in process_value(stone_value):
        count = stone_count(value, iterations_left - 1)
        stone_count_cache[value][iterations_left - 1] = count
        total_stones += count
    return total_stones


def total_stone_count(initial_stones: list[int], total_iterations: int) -> list[int]:
    return sum(stone_count(stone, total_iterations) for stone in initial_stones)


def solve(inputs: str):
    stones = list(map(int, inputs.split()))

    print(f"Part 1: {total_stone_count(stones, 25)}")
    print(f"Part 2: {total_stone_count(stones, 75)}\n")


solve(example_input)
solve(actual_input)
