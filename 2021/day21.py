"""https://adventofcode.com/2021/day/21"""

from itertools import product
from functools import cache

from utils import print_time_taken


sample_input = (4, 8)
actual_input = (3, 5)

BOARD_SIZE = 10
WINNING_SCORE = 21
DIE_ROLLS = [i for i in product([1, 2, 3], [1, 2, 3], [1, 2, 3])]
PLAYER1, PLAYER2 = 0, 1


class DiracDice:
    def __init__(self) -> None:
        self.next_roll = 1

    def roll_dice(self):
        dice_total = 0
        for _ in range(3):
            dice_total += self.next_roll
            self.next_roll = (self.next_roll % 100) + 1
        return dice_total

    def play(self, p1_start, p2_start):
        p1, p2 = p1_start, p2_start
        p1_score, p2_score = 0, 0
        die_rolls = 0

        while True:
            die_rolls += 1
            p1 += self.roll_dice()
            p1_score += (p1 - 1) % BOARD_SIZE + 1
            if p1_score >= 1000:
                break
            die_rolls += 1
            p2 += self.roll_dice()
            p2_score += (p2 - 1) % BOARD_SIZE + 1
            if p2_score >= 1000:
                break

        return min(p1_score, p2_score) * die_rolls * 3


@cache
def play_round(player1, player2, current_player, die_roll):
    total_wins = [0, 0]

    position, score = player1 if current_player == PLAYER1 else player2
    position = (position + die_roll) % 10
    score += position + 1
    if score >= WINNING_SCORE:
        total_wins[current_player] += 1
        return total_wins
    if current_player == PLAYER1:
        player1 = (position, score)
    else:
        player2 = (position, score)

    for roll in DIE_ROLLS:
        p1_wins, p2_wins = play_round(player1, player2, not current_player, sum(roll))
        total_wins[PLAYER1] += p1_wins
        total_wins[PLAYER2] += p2_wins

    return total_wins


@print_time_taken
def solve(p1_start, p2_start):

    print(f"Part 1: {DiracDice().play(p1_start, p2_start)}")

    player1_wins, player2_wins = 0, 0
    for roll in DIE_ROLLS:
        p1_wins, p2_wins = play_round(
            (p1_start - 1, 0), (p2_start - 1, 0), PLAYER1, sum(roll)
        )
        player1_wins += p1_wins
        player2_wins += p2_wins

    print(f"Part 2: {max(player1_wins, player2_wins)}\n")


solve(*sample_input)
solve(*actual_input)
