import re
import string

from aoc_utils import get_input_data

actual_input = get_input_data(2015, 11)

TWO_PAIRS = re.compile(r"(\w)(\1)\w*(\w)(\3)")
SEQ = re.compile("|".join((string.ascii_lowercase[i : i + 3] for i in range(24))))
ILLEGAL_LETTERS = "ilo"


def increment_password(password):
    def increment_character(c):
        if c == "z":
            return "a"
        c = chr(ord(c) + 1)
        if c in ILLEGAL_LETTERS:
            c = increment_character(c)
        return c

    i = len(password) - 1
    while True:
        next_character = increment_character(password[i])
        password = password[:i] + next_character + password[i + 1 :]
        if next_character != "a":
            break
        i = i - 1

    return password


def next_valid_password(password):
    while True:
        password = increment_password(password)
        if TWO_PAIRS.search(password) and SEQ.search(password):
            break
    return password


def solve(password):
    password = next_valid_password(password)
    print(f"Part 1: {password}")
    print(f"Part 2: {next_valid_password(password)}\n")


solve(actual_input)
