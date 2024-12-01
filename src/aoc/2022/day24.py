"""https://adventofcode.com/2022/day/24"""

from __future__ import annotations

import math
import os

from collections import defaultdict
from heapq import heappop, heappush

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day24_input.txt")) as f:
    actual_input = f.read()


sample_input = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""


LEFT, RIGHT, UP, DOWN, WAIT = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
MOVES = (LEFT, RIGHT, UP, DOWN, WAIT)


Xy = tuple[int, int]


class Valley:
    BLIZZARD_FLAGS = {"<": 1, ">": 2, "^": 4, "v": 8}
    BLIZZARDS = {1: LEFT, 2: RIGHT, 4: UP, 8: DOWN}

    def __init__(
        self, blizzards: dict[Xy, int], walls: set[Xy], width: int, height: int
    ) -> None:
        self.blizzards: dict[Xy, int] = blizzards
        self.walls: set[Xy] = walls
        self.width: int = width
        self.height: int = height
        self.blocked: set[Xy] = set(self.walls)
        for x in range(self.width):
            if x != 1:
                self.blocked.add((x, 0))
            if x != self.width - 2:
                self.blocked.add((x, self.height - 1))
        for y in range(1, self.height - 2):
            self.blocked.add((0, y))
            self.blocked.add((self.width - 1, y))
        self.blocked.add((1, -1))
        self.blocked.add((self.width - 2, self.height))
        self.blocked |= set(k for k, v in blizzards.items() if v)

    @classmethod
    def from_inputs(cls, inputs: str) -> Valley:
        rows = list(inputs.splitlines())
        width, height = len(rows[0]), len(rows)
        walls: set[Xy] = set()
        blizzards: defaultdict[Xy, int] = defaultdict(int)
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == "#":
                    walls.add((x, y))
                if c in cls.BLIZZARD_FLAGS:
                    blizzards[(x, y)] |= cls.BLIZZARD_FLAGS[c]
        return cls(dict(blizzards), walls, width, height)

    @classmethod
    def updated_valley(cls, valley: Valley) -> Valley:
        width, height, walls = valley.width, valley.height, valley.walls
        updated_blizzards: defaultdict[Xy, int] = defaultdict(int)
        for (x, y), flow in valley.blizzards.items():
            for mask, (dx, dy) in cls.BLIZZARDS.items():
                if flow & mask:
                    bx, by = x + dx, y + dy
                    bx = 1 if bx == width - 1 else width - 2 if bx == 0 else bx
                    by = 1 if by == height - 1 else height - 2 if by == 0 else by
                    assert (bx, by) not in walls
                    updated_blizzards[(bx, by)] |= mask
        return cls(updated_blizzards, walls, width, height)


State = tuple[int, Xy]  # State records point in cycle and the expedition's location

import math


def navigate_valley(
    valley_states: dict[int, Valley], cycle: int, start: Xy, target: Xy
) -> tuple[int, int]:
    initial_valley = valley_states[cycle]
    cycle_length = math.lcm((initial_valley.width - 2), (initial_valley.height - 2))

    visited: set[State] = set()
    g_scores: dict[State, int] = {(cycle, start): 0}
    queue: list[tuple[float, State]] = []
    heappush(queue, (0, (cycle, start)))
    while queue:
        _, state = heappop(queue)
        cycle, (x, y) = state
        if (x, y) == target:
            return g_scores[state], cycle
        visited.add(state)
        next_cycle = (cycle + 1) % cycle_length
        try:
            next_valley = valley_states[next_cycle]
        except KeyError:
            next_valley = Valley.updated_valley(valley_states[cycle])
            valley_states[next_cycle] = next_valley
        possible_moves = [(x + dx, y + dy) for dx, dy in MOVES]
        for next_xy in (m for m in possible_moves if m not in next_valley.blocked):
            next_state = (next_cycle, next_xy)
            g_score = g_scores[state] + 1
            if next_state not in g_scores or g_score < g_scores[next_state]:
                g_scores[next_state] = g_score
                h_score = abs(target[0] - next_xy[0]) + abs(target[1] - next_xy[1])
                f_score = g_score + h_score
                heappush(queue, (f_score, next_state))

    raise ValueError("No path found")


@print_time_taken
def solve(inputs: str) -> None:
    initial_valley = Valley.from_inputs(inputs)
    valley_states = {0: initial_valley}
    start, end = (1, 0), (initial_valley.width - 2, initial_valley.height - 1)

    travel_time, cycle = navigate_valley(valley_states, 0, start, end)
    print(f"Part 1: {travel_time}")

    time_to_go_back, cycle = navigate_valley(valley_states, cycle, end, start)
    time_to_return, _ = navigate_valley(valley_states, cycle, start, end)
    print(f"Part 2: {travel_time + time_to_go_back + time_to_return}\n")


solve(sample_input)
solve(actual_input)
