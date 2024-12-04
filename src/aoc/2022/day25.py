"""https://adventofcode.com/2022/day/25"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day25_input.txt")) as f:
    actual_input = f.read()


example_input = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


def decode(snafu: str) -> int:
    return sum(
        (5**i) * {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}[digit]
        for i, digit in enumerate(snafu[::-1])
    )


def encode(value: int) -> str:
    power = 0
    while (5**power) * 2 < value:
        power += 1
    digits = {p: 0 for p in range(power, -1, -1)}
    while remainder := value - sum(v * (5**p) for p, v in digits.items()):
        proposed_digit = remainder // (5**power)
        if proposed_digit < -2:
            d = power + 1
            while digits[d] == -2:
                d += 1
            digits[d] -= 1
            continue
        if proposed_digit > 2:
            d = power + 1
            while digits[d] == 2:
                d += 1
            digits[d] += 1
            continue
        digits[power] = proposed_digit
        power -= 1
    return "".join({-2: "=", -1: "-"}.get(d, str(d)) for d in digits.values())


def solve(inputs: str) -> None:
    total = sum(decode(snafu) for snafu in inputs.splitlines())
    print(f"Part 1: {encode(total)}")


solve(example_input)
solve(actual_input)
