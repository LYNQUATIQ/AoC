import os

from collections import deque

from utils import print_time_taken


with open(os.path.join(os.path.dirname(__file__), f"inputs/day22_input.txt")) as f:
    actual_input = f.read()

sample_input = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""


def play_recursive_combat(deck1, deck2):
    seen_before1, seen_before2 = set(), set()
    while deck1 and deck2:
        if tuple(deck1) in seen_before1 or tuple(deck2) in seen_before2:
            return (deck1, deque([]))
        seen_before1.add(tuple(deck1))
        seen_before2.add(tuple(deck2))

        card1, card2 = deck1.popleft(), deck2.popleft()
        one_winner = card1 > card2

        if len(deck1) >= card1 and len(deck2) >= card2:
            sub_deck1, sub_deck2 = play_recursive_combat(
                deque(list(deck1)[:card1]), deque(list(deck2)[:card2])
            )
            one_winner = len(sub_deck1) > len(sub_deck2)

        deck1.extend((card1, card2)) if one_winner else deck2.extend((card2, card1))

    return (deck1, deck2)


def calculate_winning_score(deck1, deck2):
    winner = deck1 if len(deck1) > len(deck2) else deck2
    winner.reverse()
    return sum(c * i for c, i in zip(winner, range(1, len(winner) + 1)))


@print_time_taken
def solve(inputs):
    deck1, deck2 = (deque(map(int, x.splitlines()[1:])) for x in inputs.split("\n\n"))
    while deck1 and deck2:
        card1, card2 = deck1.popleft(), deck2.popleft()
        deck1.extend((card1, card2)) if card1 > card2 else deck2.extend((card2, card1))
    print(f"Part 1: {calculate_winning_score(deck1, deck2)}")

    deck1, deck2 = (deque(map(int, x.splitlines()[1:])) for x in inputs.split("\n\n"))
    deck1, deck2 = play_recursive_combat(deck1, deck2)
    print(f"Part 2: {calculate_winning_score(deck1, deck2)}\n")


solve(sample_input)
solve(actual_input)
