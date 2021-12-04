from collections.abc import Sequence
import os

from utils import flatten, print_time_taken

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


class BingoBoard:
    def __init__(self, lines: list[str]) -> None:
        self.rows = tuple(list(map(int, line.split())) for line in lines)
        self.columns = tuple(zip(*self.rows))

    def is_completed(self, draws: Sequence[int]) -> bool:
        return any(all(n in draws for n in row) for row in self.rows) or any(
            all(n in draws for n in column) for column in self.columns
        )

    def final_score(self, draws: Sequence[int]) -> int:
        return draws[-1] * sum(n for n in flatten(self.rows) if n not in draws)


@print_time_taken
def solve(inputs):
    lines = inputs.splitlines()

    draws = iter(map(int, lines[0].split(",")))
    boards = {BingoBoard(lines[i : i + 5]) for i in range(2, len(lines), 6)}

    final_scores, drawn_numbers = [], []
    while boards:
        drawn_numbers.append(next(draws))
        for board in tuple(boards):
            if board.is_completed(drawn_numbers):
                final_scores.append(board.final_score(drawn_numbers))
                boards.discard(board)

    print(f"Part 1: {final_scores[0]}")
    print(f"Part 2: {final_scores[-1]}\n")


solve(sample_input)
solve(actual_input)
