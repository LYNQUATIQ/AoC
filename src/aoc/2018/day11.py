"""https://adventofcode.com/2018/day/11"""

from collections import defaultdict
from itertools import product
from utils import print_time_taken


def maximum_power(cum_power, size: int) -> tuple[int, tuple[int, int, int]]:
    max_power, corner = 0, (0, 0)
    for x, y in product(range(1, 302 - size), range(1, 302 - size)):
        power = cum_power[x + size - 1][y + size - 1]
        if x > 1:
            power -= cum_power[x - 1][y + size - 1]
        if y > 1:
            power -= cum_power[x + size - 1][y - 1]
        if x > 1 and y > 1:
            power += cum_power[x - 1][y - 1]
        if power > max_power:
            max_power, corner = power, (x, y)
    return max_power, (*corner, size)


@print_time_taken
def solve(grid_serial_number):
    power_levels = defaultdict(dict)
    for x, y in product(range(1, 301), range(1, 301)):
        rack_id = x + 10
        power = (y * rack_id + grid_serial_number) * rack_id
        power_levels[x][y] = (power // 100) % 10 - 5

    # Preprocess cumulative power levels
    cum_power = defaultdict(dict)
    cum_power[1][1] = power_levels[1][1]
    for y in range(2, 301):
        cum_power[1][y] = power_levels[1][y] + cum_power[1][y - 1]
    for x in range(2, 301):
        cum_power[x][1] = power_levels[x][1] + cum_power[x - 1][1]
    for x, y in product(range(2, 301), range(2, 301)):
        cum_power[x][y] = (
            power_levels[x][y]
            + cum_power[x - 1][y]
            + cum_power[x][y - 1]
            - cum_power[x - 1][y - 1]
        )

    _, corner = maximum_power(cum_power, 3)
    print(f"Part 1: {corner[0]},{corner[1]}")

    max_power, best_corner = 0, None
    for size in range(1, 301):
        power, corner = maximum_power(cum_power, size)
        if power > max_power:
            max_power, best_corner = power, corner
    print(f"Part 2: {','.join(str(c) for c in best_corner)}\n")


solve(42)
solve(3031)
