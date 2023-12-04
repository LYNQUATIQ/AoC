"""https://adventofcode.com/2023/day/4"""
import os
import re
from collections import deque

with open(os.path.join(os.path.dirname(__file__), "inputs/day04_input.txt")) as f:
    actual_input = f.read()


sample_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def solve(inputs):
    scratchcards = {}
    for card in inputs.splitlines():
        header, values = card.split(":")
        card_id = int(re.search(r"\d+", header).group())
        left, right = values.split("|")
        winning_values = set(map(int, re.findall(r"\d+", left)))
        your_values = set(map(int, re.findall(r"\d+", right)))
        scratchcards[card_id] = len(winning_values & your_values)

    total = 0
    for matches in scratchcards.values():
        if matches:
            total += 2 ** (matches - 1)
    print(f"Part 1: {total}")

    total_scratchcards = {card_id: 0 for card_id in scratchcards}
    to_play = deque(scratchcards.keys())
    while to_play:
        card_id = to_play.popleft()
        try:
            total_scratchcards[card_id] += 1
        except KeyError:
            pass
        for delta in range(1, scratchcards[card_id] + 1):
            to_play.append(card_id + delta)

    print(f"Part 2: {sum(total_scratchcards.values())}\n")


solve(sample_input)
solve(actual_input)
