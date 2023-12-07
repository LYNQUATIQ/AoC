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

JOKER = "J"


def sort_key(hand: str) -> tuple[int, tuple[int, int, int, int, int]]:
    return (
        HANDS.index(tuple(sorted(Counter(hand).values(), reverse=True))),
        tuple("AKQJT98765432".index(c) for c in hand),
    )


def sort_key2(hand: str) -> tuple[int, tuple[int, int, int, int, int]]:
    counts = {
        k: v for k, v in sorted(Counter(hand).items(), key=lambda x: x[1], reverse=True)
    }
    jokers = counts.get(JOKER, 0)
    if jokers and jokers != 5:
        counts = {k: v for k, v in counts.items() if k != JOKER}
        counts[next(iter(counts))] += jokers
    return (
        HANDS.index(tuple(counts.values())),
        tuple("AKQT98765432J".index(c) for c in hand),
    )


def solve(inputs):
    hands = {}
    for line in inputs.splitlines():
        hand, bid = line.split()
        hands[hand] = int(bid)

    sorted_hands = sorted(hands.keys(), key=sort_key, reverse=True)
    winnings = sum([rank * hands[hand] for rank, hand in enumerate(sorted_hands, 1)])
    print(f"Part 1: {winnings}")

    sorted_hands = sorted(hands.keys(), key=sort_key2, reverse=True)
    winnings = sum([rank * hands[hand] for rank, hand in enumerate(sorted_hands, 1)])
    print(f"Part 2: {winnings}\n")


solve(sample_input)
solve(actual_input)
