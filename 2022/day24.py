"""https://adventofcode.com/2022/day/24"""
from __future__ import annotations
import os

from heapq import heappop, heappush
from utils import print_time_taken
from functools import lru_cache

with open(os.path.join(os.path.dirname(__file__), f"inputs/day24_input.txt")) as f:
    actual_input = f.read()


sample_input = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
# sample_input = """#.####
# #....#
# #.>..#
# #..v.#
# #....#
# #....#
# ####.#"""
LEFT, RIGHT, UP, DOWN, WAIT = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
MOVES = (LEFT, RIGHT, UP, DOWN, WAIT)
BLIZZARDS = {"<": LEFT, ">": RIGHT, "^": UP, "v": DOWN}
# BLIZZARD_CHAR = {v: k for k, v in BLIZZARDS.items()}

OPEN, WALL, EXPEDITION = ".", "#", "E"

from dataclasses import dataclass

Xy = tuple[int, int]


@dataclass
class Valley:
    blizzards: dict[Xy, set[Xy]]
    width: int
    height: int

    def __init__(self, blizzards: dict[Xy, set[Xy]], width: int, height: int) -> None:
        self.blizzards = blizzards
        self.width = width
        self.height = height
        self.blocked = set()
        for x in range(self.width):
            if x != 1:
                self.blocked.add((x, 0))
            if x != self.width - 2:
                self.blocked.add((x, self.height - 1))
        for y in range(1, self.height - 2):
            self.blocked.add((0, y))
            self.blocked.add((self.width - 1, y))
        self.blocked.add((1, -1))
        for flows in self.blizzards.values():
            for xy in flows:
                self.blocked.add(xy)

    @classmethod
    def from_inputs(cls, inputs: str) -> Valley:
        rows = list(inputs.splitlines())
        width, height = len(rows[0]), len(rows)
        blizzards: dict[Xy, set[Xy]] = {d: set() for d in (LEFT, RIGHT, UP, DOWN)}
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c in BLIZZARDS:
                    blizzards[BLIZZARDS[c]].add((x, y))
        return cls(blizzards, width, height)

    @classmethod
    def updated_valley(cls, valley: Valley) -> Valley:
        width, height = valley.width, valley.height
        updated_blizzards: dict[Xy, set[Xy]] = {
            d: set() for d in (LEFT, RIGHT, UP, DOWN)
        }
        for (dx, dy), blizzards in valley.blizzards.items():
            for x, y in blizzards:
                x, y = x + dx, y + dy
                x = 1 if x == width - 1 else width - 2 if x == 0 else x
                y = 1 if y == height - 1 else height - 2 if y == 0 else y
                updated_blizzards[(dx, dy)].add((x, y))
        return cls(updated_blizzards, width, height)

    # def __str__(self) -> str:
    #     rows = [[WALL] * self.width]
    #     for _ in range(self.height - 2):
    #         rows.append([WALL] + [OPEN] * (self.width - 2) + [WALL])
    #     rows.append([WALL] * self.width)
    #     rows[0][1] = OPEN
    #     rows[self.height - 1][self.width - 2] = OPEN
    #     for direction, blizzards in self.blizzards.items():
    #         for x, y in blizzards:
    #             rows[y][x] = BLIZZARD_CHAR[direction] if rows[y][x] == OPEN else "*"
    #     return "\n".join("".join(r) for r in rows) + "\n"


# State records the point in the blizzard cycle and the expedition's location
State = tuple[int, Xy]


@print_time_taken
def navigate_valley(inputs: str) -> int:
    valley = Valley.from_inputs(inputs)
    start, target = (1, 0), (valley.width - 2, valley.height - 1)
    h_score = lambda xy: abs(target[0] - xy[0]) + abs(target[1] - xy[1])

    cycle_length = (valley.width - 2) * (valley.height - 2)
    valley_states = {0: valley}

    visited: set[State] = set()
    g_scores: dict[State, int] = {(0, start): 0}
    possible_times: dict[int, int] = {}
    best_time = 9_999_999_999
    queue: list[tuple[float, State]] = []
    heappush(queue, (0 + h_score(start), (0, start)))
    while queue:
        _, state = heappop(queue)
        cycle, (x, y) = state
        if (x, y) == target:
            possible_times[cycle] = g_scores[state]
            best_time = min(possible_times.values())
            break  # continue
        if g_scores[state] >= best_time:
            continue
        visited.add(state)
        next_cycle = (cycle + 1) % cycle_length
        try:
            next_valley_state = valley_states[next_cycle]
        except KeyError:
            next_valley_state = Valley.updated_valley(valley_states[cycle])
            valley_states[next_cycle] = next_valley_state
        moves = [(x + dx, y + dy) for dx, dy in MOVES]
        for next_xy in (m for m in moves if m not in next_valley_state.blocked):
            next_state = (next_cycle, next_xy)
            time_to_here = g_scores[state] + 1
            if next_state not in g_scores or time_to_here < g_scores[next_state]:
                g_scores[next_state] = time_to_here
                f_score = time_to_here + h_score(next_xy)
                heappush(queue, (f_score, next_state))
    if not possible_times:
        raise ValueError("No path found")
    return best_time


def solve(inputs: str) -> None:

    print(f"Part 1: {navigate_valley(inputs)}")
    print(f"Part 2: {False}\n")


# 199 too low
solve(sample_input)
solve(actual_input)
