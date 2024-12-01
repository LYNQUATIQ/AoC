"""https://adventofcode.com/2021/day/24"""

import os
from functools import lru_cache

with open(os.path.join(os.path.dirname(__file__), "inputs/day24_input.txt")) as f:
    actual_input = f.read()

Z_BASE, FLAG_DELTA, Z_DELTA = 0, 1, 2
PARAMS = tuple(
    tuple(
        int(instruction.split(" ")[-1])
        for i, instruction in enumerate(routine.splitlines())
        if i in (3, 4, 14)  # Lines where we find Z_BASE, FLAG_DELTA, and Z_DELTA
    )
    for routine in actual_input.split("inp w\n")[1:]
)
DIGITS_1_TO_9 = tuple(range(1, 10))
DIGITS_9_TO_1 = tuple(reversed(DIGITS_1_TO_9))


@lru_cache(maxsize=None)
def get_next_z(w: int, z: int, args: tuple[int, int, int]) -> int | None:
    """Return the next value of z based on input w and arguments.
    In cases where Z_BASE is 26 we pop a digit *unless* flag is 1 in which case we
    remultiply by 26. We therefore *need* flag too be 0 to ensure we pop digit,
    (as well as needing constants to tie up) or no chance of being zero at end!
    If flag is not 0 and Z_BASE is 26, we can return None and prune that path.
    """
    flag = int(((z % 26) + args[FLAG_DELTA]) != w)
    if args[Z_BASE] == 26 and flag:
        return None  # Pruning (when flag is 1 and Z_BASE is 26)

    z = z // args[Z_BASE]
    z *= 25 * flag + 1
    z += (w + args[Z_DELTA]) * flag
    return z


def find_result(ordered_inputs, z=0, digits=[]):
    digit_count = len(digits)
    if digit_count == 14:
        if z == 0:  # Success!
            return "".join(map(str, digits))
        return None

    for w in ordered_inputs:
        next_z = get_next_z(w, z, PARAMS[digit_count])
        if next_z is None:
            continue  # Pruning (when flag is 1 and Z_BASE is 26)
        result = find_result(ordered_inputs, next_z, digits + [w])
        if result:
            return result


def solve():
    print(f"Part 1: {find_result(DIGITS_9_TO_1)}")
    print(f"Part 2: {find_result(DIGITS_1_TO_9)}\n")


solve()
