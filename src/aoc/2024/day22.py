"""https://adventofcode.com/2024/day/22"""

from collections import defaultdict

from aoc_utils import get_input_data, print_time_taken

actual_input = get_input_data(2024, 22)
example_input = """1
10
100
2024"""

MODULO = 16777216


def evolve_secret(secret: int) -> int:
    secret ^= 64 * secret % MODULO
    secret ^= secret // 32
    secret ^= 2048 * secret % MODULO
    return secret


def gather_price_series(initial_secret: int):
    price_series = [initial_secret % 10]
    secret = initial_secret
    for _ in range(2000):
        secret = evolve_secret(secret)
        price_series.append(secret % 10)
    return secret, price_series


def get_offers(price_series):
    offers = {}
    price_deltas = [(b, b - a) for a, b in zip(price_series[:-1], price_series[1:])]
    for i, (price, d4) in enumerate(price_deltas[3:], start=3):
        d1 = price_deltas[i - 3][1]
        d2 = price_deltas[i - 2][1]
        d3 = price_deltas[i - 1][1]
        price_key = (d1, d2, d3, d4)
        offers[price_key] = offers.get(price_key, price)
    return offers


@print_time_taken
def solve(inputs: str):
    initial_secrets = tuple(map(int, inputs.splitlines()))

    total = 0
    all_price_series = []
    for secret in initial_secrets:
        last_secret, prices = gather_price_series(secret)
        total += last_secret
        all_price_series.append(prices)

    print(f"Part 1: {total}")

    all_offers = defaultdict(int)
    for prices in all_price_series:
        offers = get_offers(prices)
        for offer, price in offers.items():
            all_offers[offer] += price

    print(f"Part 2: {max(all_offers.values())}\n")


solve(example_input)
solve(actual_input)
