import os

from collections import deque

from utils import print_time_taken


with open(os.path.join(os.path.dirname(__file__), "inputs/day22_input.txt")) as f:
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


def play_recursive(deck1, deck2):
    seen_before1, seen_before2 = set(), set()
    while deck1 and deck2:
        if tuple(deck1) in seen_before1 or tuple(deck2) in seen_before2:
            return (deck1, ())
        seen_before1.add(tuple(deck1)), seen_before2.add(tuple(deck2))

        c1, c2 = deck1.popleft(), deck2.popleft()
        one_winner = c1 > c2
        if len(deck1) >= c1 and len(deck2) >= c2:
            r1, r2 = play_recursive(deque(list(deck1)[:c1]), deque(list(deck2)[:c2]))
            one_winner = len(r1) > len(r2)

        deck1.extend((c1, c2)) if one_winner else deck2.extend((c2, c1))

    return (deck1, deck2)


def calculate_score(deck1, deck2):
    winner = deck1 if len(deck1) > len(deck2) else deck2
    return sum(c * i for c, i in zip(winner, range(len(winner), 0, -1)))


@print_time_taken
def solve(inputs):
    deck1, deck2 = (deque(map(int, x.splitlines()[1:])) for x in inputs.split("\n\n"))

    while deck1 and deck2:
        card1, card2 = deck1.popleft(), deck2.popleft()
        deck1.extend((card1, card2)) if card1 > card2 else deck2.extend((card2, card1))
    print(f"Part 1: {calculate_score(deck1, deck2)}")

    deck1, deck2 = (deque(map(int, x.splitlines()[1:])) for x in inputs.split("\n\n"))
    print(f"Part 2: {calculate_score(*play_recursive(deck1, deck2))}\n")


solve(sample_input)
solve(actual_input)
