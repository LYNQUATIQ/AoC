"""https://adventofcode.com/2021/day/23"""
import os
import re

from collections import defaultdict
from functools import lru_cache
from heapq import heappush, heappop
from itertools import product
from typing import TypeAlias

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day23_input.txt")) as f:
    actual_input = f.read()


sample_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""


AMBER, BRONZE, COPPER, DESERT = "A", "B", "C", "D"
AMPHIPODS = (AMBER, BRONZE, COPPER, DESERT)
ENERGY = {AMBER: 1, BRONZE: 10, COPPER: 100, DESERT: 1000}

BURROW_LENGTH = 11
AMPHIPOD_ROOMS = {AMBER: 2, BRONZE: 4, COPPER: 6, DESERT: 8}
HALLWAY_POSITIONS = tuple(i for i in range(11) if i not in AMPHIPOD_ROOMS.values())
BETWEEN = {
    (s, d): tuple(h for h in HALLWAY_POSITIONS if s < h < d or d < h < s)
    for s, d in product(range(BURROW_LENGTH), range(BURROW_LENGTH))
    if s != d
}

Amphipod: TypeAlias = str  # 'A', 'B', 'C' or 'D'
HallwayAmphipods: TypeAlias = tuple[tuple[Amphipod, int], ...]
RoomAmphipods: TypeAlias = list[
    tuple[Amphipod, ...],
    tuple[Amphipod, ...],
    tuple[Amphipod, ...],
    tuple[Amphipod, ...],
]

# State is energy so far, estimated cost to complete, and amphipods in rooms and halls
State: TypeAlias = tuple[int, int, RoomAmphipods, HallwayAmphipods]


@lru_cache(maxsize=None)
def possible_next_states(state: State) -> list[State]:
    (energy_so_far, cost_to_complete, room_amphipods, hallway_amphipods) = state
    blocked = {h for _, h in hallway_amphipods}
    available = {h for h in HALLWAY_POSITIONS if h not in blocked}

    next_states = []

    # Try and move amphipods in rooms out to the hall
    for i, occupants in enumerate(room_amphipods):
        if not occupants:
            continue
        start = (i + 1) * 2
        for destination in available:
            if any(h in blocked for h in BETWEEN[(start, destination)]):
                continue  # There's somebody blocking the way en route to h
            amphipod = occupants[0]
            target = AMPHIPOD_ROOMS[amphipod]
            steps_sd = abs(start - destination) + 1  # Extra step to leave room
            steps_dt = abs(target - destination) + 1  # Extra step to enter room
            steps_st = abs(target - start) + 1 + 1  # Extra *steps* to leave/enter rooms
            step_change = steps_dt - steps_st
            next_states.append(
                (
                    energy_so_far + steps_sd * ENERGY[amphipod],
                    cost_to_complete + step_change * ENERGY[amphipod],
                    (*room_amphipods[:i], occupants[1:], *room_amphipods[i + 1 :]),
                    ((amphipod, destination), *hallway_amphipods),
                )
            )

    # Try and move amphipods in hallway to their destination
    for amphipod, start in hallway_amphipods:
        destination = AMPHIPOD_ROOMS[amphipod]
        if room_amphipods[destination // 2 - 1]:
            continue  # There's somebody in the room who still needs to move
        if any(h in blocked for h in BETWEEN[(start, destination)]):
            continue  # There's somebody blocking the way en route to target
        energy_change = (abs(start - destination) + 1) * ENERGY[amphipod]
        next_states.append(
            (
                energy_so_far + energy_change,
                cost_to_complete - energy_change,
                room_amphipods,
                tuple((a, h) for a, h in hallway_amphipods if h != start),
            )
        )

    return next_states


def organise_amphipods(
    amphipod_rows: tuple[tuple[Amphipod, Amphipod, Amphipod, Amphipod], ...]
) -> int:

    extra_energy, amphipod_count = 0, defaultdict(int)

    # Build room tuples, stripping out any amphipods who are already in place.
    # Also calculate extra energy required as amphipods leave their starting rooms...
    room_occupants = defaultdict(list)
    for amphipods in amphipod_rows:
        for room_variant, amphipod in zip(AMPHIPODS, amphipods):
            room_occupants[room_variant].append(amphipod)
    for room_variant, occupants in room_occupants.items():
        while occupants and occupants[-1] == room_variant:
            occupants.pop()
        for position_in_room, amphipod in enumerate(occupants):
            amphipod_count[amphipod] += 1
            extra_energy += ENERGY[amphipod] * position_in_room

    # ...and add extra energy required for amphipods arriving at their destination
    for variant, count in amphipod_count.items():
        extra_energy += ENERGY[variant] * {1: 0, 2: 1, 3: 3, 4: 6}[count]

    room_amphipods = tuple(tuple(occupants) for occupants in room_occupants.values())

    # Calculate the initial estimated 'cost to complete' (assumed everyone moves direct)
    cost_to_complete = 0
    for i, occupants in enumerate(room_amphipods):
        cost_to_complete += sum(
            (abs(AMPHIPOD_ROOMS[a] - ((i + 1) * 2)) + 2) * ENERGY[a] for a in occupants
        )

    initial_state = (0, cost_to_complete, tuple(room_amphipods), ())
    to_visit = [(cost_to_complete, initial_state)]

    while to_visit:
        _, state = heappop(to_visit)
        energy_so_far, cost_to_complete, _, _ = state
        if cost_to_complete == 0:
            return energy_so_far + extra_energy
        for next_state in possible_next_states(state):
            heappush(to_visit, (next_state[0] + next_state[1], next_state))

    return None


EXTRA_ROWS = (("D", "C", "B", "A"), ("D", "B", "A", "C"))


@print_time_taken
def solve(inputs):

    amphipod_data = inputs.splitlines()
    first_row = tuple(re.findall(r"[ABCD]", amphipod_data[2]))
    last_row = tuple(re.findall(r"[ABCD]", amphipod_data[3]))

    print(f"Part 1: {organise_amphipods((first_row, last_row))}")
    # print(f"Part 2: {organise_amphipods( (first_row, *EXTRA_ROWS, last_row))}\n")


solve(sample_input)
solve(actual_input)
