"""https://adventofcode.com/2022/day/25"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day25_input.txt")) as f:
    actual_input = f.read()


sample_input = """1=-0-2
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


def solve(inputs: str) -> None:
    total = 0
    for snafu in inputs.splitlines():
        value = 0
        for i, token in enumerate(snafu[::-1]):
            if token == "=":
                digit = -2
            elif token == "-":
                digit = -1
            else:
                digit = int(token)
            value += (5 ** i) * digit
        total += value

    power = 0
    while (5 ** power) * 2 < total:
        power += 1

    digits = {p: 0 for p in range(power, -1, -1)}

    def remainder():
        return total - sum(v * (5 ** p) for p, v in digits.items())

    while remainder() != 0:
        proposed_digit = remainder() // (5 ** power)
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
        continue

    snafu = "".join({-2: "=", -1: "-"}.get(d, str(d)) for d in digits.values())
    print(f"Part 1: {snafu}")


solve(sample_input)
solve(actual_input)
