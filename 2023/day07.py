"""https://adventofcode.com/2023/day/7"""
import os
from collections import Counter

with open(os.path.join(os.path.dirname(__file__), "inputs/day07_input.txt")) as f:
    actual_input = f.read()


sample_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

HANDS = [
    (5,),
    (4, 1),
    (3, 2),
    (3, 1, 1),
    (2, 2, 1),
    (2, 1, 1, 1),
    (1, 1, 1, 1, 1),
]

CARDS = "AKQJT9876543210"
CARDS2 = "AKQT9876543210J"
JOKER = "J"


def solve(inputs):
    hands = {}
    for line in inputs.splitlines():
        hand, bid = line.split()
        hands[hand] = int(bid)

    def sort_key(hand: str) -> tuple[int, str]:
        return (
            HANDS.index(tuple(sorted(Counter(hand).values(), reverse=True))),
            tuple(CARDS.index(c) for c in hand),
        )

    sorted_hands = {
        k: hands[k] for k in sorted(hands.keys(), key=sort_key, reverse=True)
    }

    total = 0
    for rank, bid in enumerate(sorted_hands.values(), 1):
        total += rank * bid
    print(f"Part 1: {total}")

    def sort_key2(hand: str) -> tuple[int, str]:
        counts = {
            k: v
            for k, v in sorted(Counter(hand).items(), key=lambda x: x[1], reverse=True)
        }
        jokers = counts.get(JOKER, 0)
        if jokers and jokers != 5:
            counts = {k: v for k, v in counts.items() if k != JOKER}
            counts[list(counts.keys())[0]] += jokers
        return (
            HANDS.index(tuple(sorted(counts.values(), reverse=True))),
            tuple(CARDS2.index(c) for c in hand),
        )

    sorted_hands = {
        k: hands[k] for k in sorted(hands.keys(), key=sort_key2, reverse=True)
    }

    total = 0
    for rank, bid in enumerate(sorted_hands.values(), 1):
        total += rank * bid
    print(f"Part 2: {total}\n")


solve(sample_input)
solve(actual_input)
