# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter
from itertools import product

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day04.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/day04_input.txt")) as f:
    actual_input = f.read()

sample_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

BOARD_SIZE = 5


class Board:
    def __init__(self, lines) -> None:
        self.rows = tuple(list(map(int, line.split())) for line in lines)
        self.columns = tuple(zip(*self.rows))
        self.drawn_numbers = set()
        self.final_score = None

    def __repr__(self) -> str:
        return "\n".join(str(row) for row in self.rows)

    def _is_completed(self) -> bool:
        for i in range(BOARD_SIZE):
            if all(n in self.drawn_numbers for n in self.rows[i]):
                return True
            if all(n in self.drawn_numbers for n in self.columns[i]):
                return True
        return False

    def add_draw(self, draw: int) -> bool:
        if not self.final_score:
            self.drawn_numbers.add(draw)
            if self._is_completed():
                self.final_score = draw * sum(
                    n for n in flatten(self.rows) if n not in self.drawn_numbers
                )
                return True
        return False


@print_time_taken
def solve(inputs):
    lines = inputs.splitlines()
    numbers = map(int, lines[0].split(","))

    boards = []
    for i in range(2, len(lines), BOARD_SIZE + 1):
        boards.append(Board(lines[i : i + BOARD_SIZE]))

    first_board, last_board = None, None
    for draw in numbers:
        for board in boards:
            if board.add_draw(draw):
                first_board = first_board or board
                last_board = board

    print(f"Part 1: {first_board.final_score}")
    print(f"Part 2: {last_board.final_score}\n")


solve(sample_input)
solve(actual_input)
