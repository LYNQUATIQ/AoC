"""https://adventofcode.com/2021/day/24"""
from functools import lru_cache

from utils import print_time_taken


PARAMS = [
    (1, 14, 14),
    (1, 14, 2),
    (1, 14, 1),
    (1, 12, 13),
    (1, 15, 5),
    (26, -12, 5),
    (26, -12, 5),
    (1, 12, 9),
    (26, -7, 3),
    (1, 13, 13),
    (26, -8, 2),
    (26, -5, 1),
    (26, -10, 11),
    (26, -7, 8),
]


@lru_cache(maxsize=None)
def get_next_z(w: int, z: int, z_div: int, xc: int, yc: int) -> int | None:

    # N.B. When z_div is 1, xc is *always* > 10, therefore flag is 1 in all cases
    # and code reduces to:
    #     new_z = z * 26 + (digit + yc)   ...essentially pushing a digit in base 26
    #
    # In cases where z_div is 26 we pop a digit *unless* flag is 1 in which case we
    # remultiply by 26. We therefore *need* flag too be 0 to ensure we pop digit,
    # (as well as needing constants to tie up) or no chance of being zero at end!
    flag = int(((z % 26) + xc) != w)
    if z_div == 26 and flag:
        return None

    z = z // z_div
    y = 25 * flag + 1
    z *= 25 * flag + 1
    z += (w + yc) * flag
    return z


def find_result(digits, so_far=[], z=0):
    num_digits = len(so_far)

    if num_digits == 14:
        if z == 0:
            return "".join(map(str, so_far))
        return None

    z_div, xc, yc = PARAMS[num_digits]
    for w in digits:
        next_z = get_next_z(w, z, z_div, xc, yc)
        if next_z is None:
            continue
        result = find_result(digits, so_far + [w], next_z)
        if result:
            return result


@print_time_taken
def solve():

    print(f"Part 1: {find_result(tuple(range(9,0,-1)))}")
    print(f"Part 2: {find_result(tuple(range(1,10)))}\n")


solve()
