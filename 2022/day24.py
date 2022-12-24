"""https://adventofcode.com/2022/day/24"""
from __future__ import annotations
import os

from collections import defaultdict
from heapq import heappop, heappush

from utils import print_time_taken

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
BLIZZARD_FLAGS = {"<": 1, ">": 2, "^": 4, "v": 8}
BLIZZARDS = {1: LEFT, 2: RIGHT, 4: UP, 8: DOWN}
MOVES = (LEFT, RIGHT, UP, DOWN, WAIT)

OPEN, WALL, EXPEDITION = ".", "#", "E"


Xy = tuple[int, int]


class Valley:
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
                if c == WALL:
                    walls.add((x, y))
                if c in BLIZZARD_FLAGS:
                    blizzards[(x, y)] |= BLIZZARD_FLAGS[c]
        return cls(dict(blizzards), walls, width, height)

    @classmethod
    def updated_valley(cls, valley: Valley) -> Valley:
        width, height, walls = valley.width, valley.height, valley.walls
        updated_blizzards: defaultdict[Xy, int] = defaultdict(int)
        for (x, y), flow in valley.blizzards.items():

            for mask, (dx, dy) in BLIZZARDS.items():
                if flow & mask:
                    bx, by = x + dx, y + dy
                    bx = 1 if bx == width - 1 else width - 2 if bx == 0 else bx
                    by = 1 if by == height - 1 else height - 2 if by == 0 else by
                    assert (bx, by) not in walls
                    updated_blizzards[(bx, by)] |= mask
        return cls(updated_blizzards, walls, width, height)

    def print(self, you: Xy) -> None:
        x0, y0 = you
        assert you not in self.walls
        assert you not in self.blizzards
        for y in range(self.height):
            for x in range(self.width):
                xy = (x, y)
                c = EXPEDITION if xy == you else WALL if xy in self.walls else OPEN
                if xy in self.blizzards:
                    c = {1: "<", 2: ">", 4: "^", 8: "v"}.get(self.blizzards[xy], "*")
                print(c, end="")
            print()


# State records the point in the blizzard cycle and the expedition's location
State = tuple[int, Xy]


@print_time_taken
def navigate_valley(
    valley_states: dict[int, Valley], cycle: int, start: Xy, target: Xy
) -> tuple[int, int]:
    initial_valley = valley_states[cycle]
    cycle_length = (initial_valley.width - 2) * (initial_valley.height - 2)

    prior_states: dict[State, State] = {}
    visited: set[State] = set()
    g_scores: dict[State, int] = {(cycle, start): 0}
    possible_times: dict[int, int] = {}
    best_time = 9_999_999_999
    queue: list[tuple[float, State]] = []
    heappush(queue, (0, (cycle, start)))
    while queue:
        _, state = heappop(queue)
        cycle, (x, y) = state
        if (x, y) == target:
            possible_times[cycle] = g_scores[state]
            best_time = min(possible_times.values())
            return g_scores[state], cycle
        if g_scores[state] >= best_time:
            continue
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
            time_to_here = g_scores[state] + 1
            if next_state not in g_scores or time_to_here < g_scores[next_state]:
                g_scores[next_state] = time_to_here
                h_score = abs(target[0] - next_xy[0]) + abs(target[1] - next_xy[1])
                f_score = time_to_here + h_score
                heappush(queue, (f_score, next_state))
                prior_states[next_state] = state

    if not possible_times:
        raise ValueError("No path found")

    max_states = [s for s, g in g_scores.items() if g == best_time and s[1] == target]
    path = [max_states[0]]
    s = path[0]
    while True:
        try:
            s = prior_states[s]
        except KeyError:
            break
        path.append(s)
    for i, (cycle_point, expedition) in enumerate(reversed(path)):
        valley = valley_states[cycle_point]
        print(f"\nMinute {i} (E={expedition})\n----------")
        valley.print(expedition)

    return g_scores[state], cycle


def solve(inputs: str) -> None:
    initial_valley = Valley.from_inputs(inputs)
    valley_states = {0: initial_valley}
    start, end = (1, 0), (initial_valley.width - 2, initial_valley.height - 1)

    travel_time, cycle = navigate_valley(valley_states, 0, start, end)
    print(f"Part 1: {travel_time}")

    total_time = travel_time
    travel_time, cycle = navigate_valley(valley_states, cycle, end, start)
    total_time += travel_time
    travel_time, cycle = navigate_valley(valley_states, cycle, start, end)
    total_time += travel_time

    print(f"Part 2: {total_time}\n")


solve(sample_input)
solve(actual_input)
