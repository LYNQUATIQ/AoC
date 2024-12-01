"""https://adventofcode.com/2023/day/1"""

import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day01_input.txt")) as f:
    actual_input = f.read()


part1_sample_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

part2_sample_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
REVERSED_DIGITS = {k[::-1]: v for k, v in DIGITS.items()}


def find_digit(text: str, digits: dict[str, int] | None = None) -> int:
    digits = {} if digits is None else digits
    for i, c in enumerate(text):
        if c.isdigit():
            return int(c)
        for k, v in digits.items():
            if text[i:].startswith(k):
                return v
    raise ValueError(f"Dodgy string: {text}")


def solve(part1_inputs, part2_inputs):
    values = [
        find_digit(line) * 10 + find_digit(line[::-1])
        for line in part1_inputs.splitlines()
    ]
    print(f"Part 1: {sum(values)}")

    values = [
        find_digit(line, DIGITS) * 10 + find_digit(line[::-1], REVERSED_DIGITS)
        for line in part2_inputs.splitlines()
    ]
    print(f"Part 2: {sum(values)}\n")


solve(part1_sample_input, part2_sample_input)
solve(actual_input, actual_input)
