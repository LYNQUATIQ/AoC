"""https://adventofcode.com/2022/day/2"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day02_input.txt")) as f:
    actual_input = f.read()

SAMPLE_INPUT = """A Y
B X
C Z
"""


ROCK, PAPER, SCISSORS = 1, 2, 3
WIN, DRAW, LOSE = 6, 3, 0

SHAPES = {"A": ROCK, "B": PAPER, "C": SCISSORS, "X": ROCK, "Y": PAPER, "Z": SCISSORS}
RESULTS = {"X": LOSE, "Y": DRAW, "Z": WIN}

# Outcomes - the result given an opponent's shape and your shape
OUTCOMES = {
    ROCK: {ROCK: DRAW, PAPER: WIN, SCISSORS: LOSE},
    PAPER: {ROCK: LOSE, PAPER: DRAW, SCISSORS: WIN},
    SCISSORS: {ROCK: WIN, PAPER: LOSE, SCISSORS: DRAW},
}

# Strategies - what to play given an opponent's shape and a desired outcome
STRATEGIES = {
    opponent: {outcome: you for you, outcome in OUTCOMES[opponent].items()}
    for opponent in (ROCK, PAPER, SCISSORS)
}


def solve(inputs: str) -> None:
    total_score = 0
    for token1, token2 in map(lambda l: l.split(), inputs.splitlines()):
        opponent, you = SHAPES[token1], SHAPES[token2]
        result = OUTCOMES[opponent][you]
        total_score += result + you
    print(f"\nPart 1: {total_score}")

    total_score = 0
    for token1, token2 in map(lambda l: l.split(), inputs.splitlines()):
        opponent, result = SHAPES[token1], RESULTS[token2]
        you = STRATEGIES[opponent][result]
        total_score += result + you
    print(f"Part 2: {total_score}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
