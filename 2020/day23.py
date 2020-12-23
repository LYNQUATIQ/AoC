import math
from utils import print_time_taken

sample_input = """389125467"""
actual_input = """135468729"""


class CupGame:
    def __init__(self, cups, total_cups=None):
        cups = list(cups)
        self.total_cups = total_cups or len(cups)
        self.cup_after = {c: cups[i + 1] for i, c in enumerate(cups[:-1])}
        self.cup_after[cups[-1]] = cups[0]
        if self.total_cups > len(cups):
            self.cup_after[total_cups] = cups[0]
            self.cup_after[cups[-1]] = len(cups) + 1
        self.current_cup = cups[0]

    def _get_cup_after(self, cup):
        return self.cup_after.get(cup, cup + 1)

    def play_rounds(self, rounds):
        for _ in range(rounds):
            pick1 = self._get_cup_after(self.current_cup)
            pick2 = self._get_cup_after(pick1)
            pick3 = self._get_cup_after(pick2)
            new_cup = self._get_cup_after(pick3)

            insert_left = self.current_cup - 1 or self.total_cups
            while insert_left in (pick1, pick2, pick3):
                insert_left = insert_left - 1 or self.total_cups
            insert_right = self._get_cup_after(insert_left)
            self.cup_after[insert_left] = pick1
            self.cup_after[pick3] = insert_right

            self.cup_after[self.current_cup] = new_cup
            self.current_cup = new_cup

    def cups_after_one(self, number_to_get=None):
        number_to_get = number_to_get or self.total_cups - 1
        cup, cups = 1, []
        for _ in range(number_to_get):
            cup = self._get_cup_after(cup)
            cups.append(cup)
        return cups


@print_time_taken
def solve(inputs):
    cups = [int(c) for c in inputs]

    cup_game = CupGame(cups)
    cup_game.play_rounds(100)
    print(f"Part 1: {''.join(str(c) for c in cup_game.cups_after_one())}")

    cup_game = CupGame(cups, 1_000_000)
    cup_game.play_rounds(10_000_000)
    print(f"Part 2: {math.prod(cup_game.cups_after_one(2))}")


solve(sample_input)
solve(actual_input)
