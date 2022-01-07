"""https://adventofcode.com/2018/day/9"""
import os
import re

from collections import defaultdict

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day09_input.txt")) as f:
    actual_input = f.read()

sample_input = """10 players; last marble is worth 1618 points"""


class Marble:
    def __init__(self, value: int) -> None:
        self.value = value
        self.clockwise, self.counter_clockwise = self, self

    def insert_clockwise_of(self, other):
        other_initial_clockwise = other.clockwise
        other.clockwise = self
        self.counter_clockwise = other
        self.clockwise = other_initial_clockwise
        other_initial_clockwise.counter_clockwise = self

    def remove(self):
        self.counter_clockwise.clockwise = self.clockwise
        self.clockwise.counter_clockwise = self.counter_clockwise
        return self.value


def play_game(num_players: int, last_marble: int):
    current_marble = Marble(0)
    scores = defaultdict(int)
    current_player = 0
    for i in range(1, last_marble + 1):
        current_player = (current_player + 1) % num_players
        if i % 23 == 0:
            scores[current_player] += i
            for _ in range(7):
                current_marble = current_marble.counter_clockwise
            scores[current_player] += current_marble.remove()
            current_marble = current_marble.clockwise
            continue
        next_marble = Marble(i)
        next_marble.insert_clockwise_of(current_marble.clockwise)
        current_marble = next_marble
    return max(scores.values())


@print_time_taken
def solve(inputs):
    num_players, last_marble = map(int, re.findall(r"\d+", inputs))
    print(f"Part 1: {play_game(num_players, last_marble)}")
    print(f"Part 2: {play_game(num_players, last_marble*100)}\n")


solve(sample_input)
solve(actual_input)
