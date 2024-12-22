"""https://adventofcode.com/2024/day/22"""

from aoc_utils import get_input_data, print_time_taken

actual_input = get_input_data(2024, 22)


example_input = """1
10
100
2024"""

MODULO = 16777216


def evolve_secret(secret: int) -> int:
    # xor secret with 64 * secret
    secret ^= 64 * secret
    secret %= MODULO
    secret ^= secret // 32
    secret %= MODULO
    secret ^= 2048 * secret
    secret %= MODULO
    return secret


@print_time_taken
def solve(inputs: str):
    initial_secrets = tuple(map(int, inputs.splitlines()))

    total = 0
    for secret in initial_secrets:
        # original_secret = secret
        for _ in range(2000):
            secret = evolve_secret(secret)
        # print(f"{original_secret}: {secret}")
        total += secret

    print(f"Part 1: {total}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
