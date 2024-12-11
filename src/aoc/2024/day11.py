"""https://adventofcode.com/2024/day/11"""

from functools import cache

actual_input = "9694820 93 54276 1304 314 664481 0 4"
example_input = "125 17"


def process_value(value: int) -> list[int]:
    if value == 0:
        return [1]
    if len(str(value)) % 2 == 0:
        lhs = int(str(value)[: len(str(value)) // 2])
        rhs = int(str(value)[len(str(value)) // 2 :])
        return [lhs, rhs]
    return [value * 2024]


@cache
def stone_count(stone_value: int, iterations_left: int) -> int:
    if iterations_left == 0:
        return 1
    return sum(stone_count(v, iterations_left - 1) for v in process_value(stone_value))


def total_stone_count(initial_stones: list[int], total_iterations: int) -> list[int]:
    return sum(stone_count(stone, total_iterations) for stone in initial_stones)


def solve(inputs: str):
    stones = list(map(int, inputs.split()))
    print(f"Part 1: {total_stone_count(stones, 25)}")
    print(f"Part 2: {total_stone_count(stones, 75)}\n")


solve(example_input)
solve(actual_input)
