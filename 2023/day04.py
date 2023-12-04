"""https://adventofcode.com/2023/day/4"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day04_input.txt")) as f:
    actual_input = f.read()


sample_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def solve(inputs):
    matches, scratchcards = [], []
    for card_id, card in enumerate(inputs.splitlines()):
        winning_numbers, numbers_you_have = map(
            lambda x: set(x.split()), card.split(":")[1].split("|")
        )
        matches.append(len(winning_numbers & numbers_you_have))
        scratchcards.append(
            1  # The original card...
            + sum(  # ...plus the total copies of the card based on prior cards' matches
                scratchcards[prior_id]
                for prior_id in range(card_id - len(winning_numbers), card_id)
                if prior_id >= 0 and (prior_id + matches[prior_id] >= card_id)
            )
        )

    print(f"Part 1: {sum(map(lambda x : 2 ** (x - 1) if x > 0 else 0, matches))}")
    print(f"Part 2: {sum(scratchcards)}\n")


solve(sample_input)
solve(actual_input)
