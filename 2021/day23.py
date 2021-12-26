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
AMPHIPOD_INDEX = {AMBER: 0, BRONZE: 1, COPPER: 2, DESERT: 3}
HALLWAY_POSITIONS = tuple(i for i in range(11) if i not in AMPHIPOD_ROOMS.values())
BETWEEN = {
    (s, d): tuple(h for h in HALLWAY_POSITIONS if s < h < d or d < h < s)
    for s, d in product(range(BURROW_LENGTH), range(BURROW_LENGTH))
    if s != d
}

Amphipod: TypeAlias = str  # 'A', 'B', 'C' or 'D'
HallwayAmphipods: TypeAlias = tuple[tuple[Amphipod, int], ...]
RoomAmphipods: TypeAlias = tuple[
    tuple[Amphipod, ...],
    tuple[Amphipod, ...],
    tuple[Amphipod, ...],
    tuple[Amphipod, ...],
]
Move: TypeAlias = tuple[Amphipod, int, int]
# State is energy so far, cost so complet, amphipods in rooms, and amphipods in halls
State: TypeAlias = tuple[int, int, RoomAmphipods, HallwayAmphipods]


@lru_cache(maxsize=None)
def possible_next_states(state: State) -> list[State]:
    (energy_so_far, cost_to_complete, room_amphipods, hallway_amphipods) = state
    blocked = {h for a, h in hallway_amphipods}
    clear_hallway = {h for h in HALLWAY_POSITIONS if h not in blocked}

    next_states = []

    # Try and move amphipods in rooms out to the hall
    for i, occupants in enumerate(room_amphipods):
        if not occupants:
            continue
        start = (i + 1) * 2
        for destination in clear_hallway:
            if any(h in blocked for h in BETWEEN[(start, destination)]):
                continue  # There's somebody blocking the way en route to h
            amphipod = occupants[0]
            target = AMPHIPOD_ROOMS[amphipod]
            steps_sd = abs(start - destination) + 1  # Extra step to leave room
            steps_st = abs(target - start) + 1 + 1  # Extra *steps* to leave/enter rooms
            steps_dt = abs(target - destination) + 1  # Extra step to enter room
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
        if room_amphipods[AMPHIPOD_INDEX[amphipod]]:
            continue  # There's somebody in the room who still needs to move
        if any(h in blocked for h in BETWEEN[(start, destination)]):
            continue  # There's somebody blocking the way en route to target
        steps_taken = abs(start - destination) + 1
        next_states.append(
            (
                energy_so_far + steps_taken * ENERGY[amphipod],
                cost_to_complete - steps_taken * ENERGY[amphipod],
                room_amphipods,
                tuple((a, h) for a, h in hallway_amphipods if h != start),
            )
        )

    return next_states


def organise_amphipods(room_amphipods: RoomAmphipods) -> int:

    # Strip out any amphipods who are already in place.
    # Also calculate extra energy required as amphipods leaving their starting rooms...
    initial_rooms = []
    extra_energy, amphipod_count = 0, defaultdict(int)
    for room_variant, occupant_tuple in zip(AMPHIPODS, room_amphipods):
        occupants = list(occupant_tuple)
        while occupants and occupants[-1] == room_variant:
            occupants.pop()
        initial_rooms.append(tuple(occupants))
        for position_in_room, amphipod in enumerate(occupants):
            amphipod_count[amphipod] += 1
            extra_energy += ENERGY[amphipod] * position_in_room

    # ...and add extra energy required for amphipods arriving at their destination
    for variant, count in amphipod_count.items():
        extra_energy += ENERGY[variant] * {1: 0, 2: 1, 3: 3, 4: 6}[count]

    room_amphipods = tuple(initial_rooms)

    cost_to_complete = 0
    for i, occupants in enumerate(room_amphipods):
        start = (i + 1) * 2
        for amphipod in occupants:
            target = AMPHIPOD_ROOMS[amphipod]
            cost_to_complete += (abs(target - start) + 2) * ENERGY[amphipod]

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
    top_row = tuple(re.findall(r"[ABCD]", amphipod_data[2]))
    bottom_row = tuple(re.findall(r"[ABCD]", amphipod_data[3]))

    def get_room_ampipods(rows) -> RoomAmphipods:
        room_list = defaultdict(list)
        for amphipods in rows:
            for room, amphipod in zip(AMPHIPODS, amphipods):
                room_list[room].append(amphipod)
        return tuple(tuple(occupants) for occupants in room_list.values())

    room_amphipods = get_room_ampipods((top_row, bottom_row))
    print(f"Part 1: {organise_amphipods(room_amphipods)}")

    # room_amphipods = get_room_ampipods((top_row, *EXTRA_ROWS, bottom_row))
    # print(f"Part 2: {organise_amphipods(room_amphipods)}\n")


solve(sample_input)
solve(actual_input)
