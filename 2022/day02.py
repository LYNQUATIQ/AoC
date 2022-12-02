"""https://adventofcode.com/2022/day/2"""
import os

from enum import IntEnum


with open(os.path.join(os.path.dirname(__file__), f"inputs/day02_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """A Y
B X
C Z
"""


ROCK, PAPER, SCISSORS = 1, 2, 3
SHAPES = {"A": ROCK, "B": PAPER, "C": SCISSORS, "X": ROCK, "Y": PAPER, "Z": SCISSORS}

WIN, DRAW, LOSE = 6, 3, 0
RESULTS = {"X": LOSE, "Y": DRAW, "Z": WIN}

OUTCOMES = {
    ROCK: {ROCK: DRAW, PAPER: LOSE, SCISSORS: WIN},
    PAPER: {ROCK: WIN, PAPER: DRAW, SCISSORS: LOSE},
    SCISSORS: {ROCK: LOSE, PAPER: WIN, SCISSORS: DRAW},
}

STRATEGIES = {
    WIN: {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK},
    DRAW: {ROCK: ROCK, PAPER: PAPER, SCISSORS: SCISSORS},
    LOSE: {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER},
}


def solve(inputs: str) -> None:
    total_score = 0
    for line in inputs.splitlines():
        token1, token2 = line.split()
        opponent, you = SHAPES[token1], SHAPES[token2]
        result = OUTCOMES[you][opponent]
        total_score += result + you
    print(f"\nPart 1: {total_score}")

    total_score = 0
    for line in inputs.splitlines():
        token1, token2 = line.split()
        opponent, result = SHAPES[token1], RESULTS[token2]
        you = STRATEGIES[result][opponent]
        total_score += result + you
    print(f"Part 2: {total_score}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
