"""https://adventofcode.com/2021/day/23"""

import os
import re

from collections import defaultdict
from functools import lru_cache
from heapq import heappush, heappop
from itertools import product
from typing import TypeAlias

with open(os.path.join(os.path.dirname(__file__), "inputs/day23_input.txt")) as f:
    actual_input = f.read()


sample_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""


HALLWAY_POSITIONS = tuple(i for i in range(11) if i not in (2, 4, 6, 8))
BETWEEN = {
    (s, d): tuple(h for h in HALLWAY_POSITIONS if s < h <= d or d <= h < s)
    for s, d in product(range(11), range(11))
    if s != d
}

# State is energy so far, estimated cost to complete, and amphipods in rooms and hallway
State: TypeAlias = tuple[int, int, tuple[tuple[int, ...]], tuple[int | None, ...]]


@lru_cache(maxsize=None)
def possible_next_states(state: State) -> list[State]:
    energy_so_far, cost_to_complete, rooms, hallway = state
    next_states = []

    # Try and move amphipods in rooms out to the hall
    for i, occupants in enumerate(rooms):
        if not occupants:
            continue
        start = (i + 1) * 2
        for destination in HALLWAY_POSITIONS:
            if any(hallway[step] is not None for step in BETWEEN[(start, destination)]):
                continue  # There's somebody blocking the way en route to destination
            amphipod = occupants[0]
            target = (amphipod + 1) * 2
            steps_sd = abs(start - destination) + 1  # Extra step to leave room
            step_change = abs(target - destination) - abs(target - start) - 1
            energy_cost = 10**amphipod
            next_states.append(
                (
                    energy_so_far + steps_sd * energy_cost,
                    cost_to_complete + step_change * energy_cost,
                    (*rooms[:i], occupants[1:], *rooms[i + 1 :]),
                    (*hallway[:destination], amphipod, *hallway[destination + 1 :]),
                )
            )

    # Try and move amphipods in hallway to their destination
    for start in (h for h in HALLWAY_POSITIONS if hallway[h] is not None):
        amphipod = hallway[start]
        destination = (amphipod + 1) * 2
        if rooms[destination // 2 - 1]:
            continue  # There's somebody in the room who still needs to move
        if any(hallway[step] is not None for step in BETWEEN[(start, destination)]):
            continue  # There's somebody blocking the way en route to target
        energy_change = (abs(start - destination) + 1) * 10**amphipod
        next_states.append(
            (
                energy_so_far + energy_change,
                cost_to_complete - energy_change,
                rooms,
                (*hallway[:start], None, *hallway[start + 1 :]),
            )
        )

    return next_states


def organise_amphipods(amphipod_rows: tuple[tuple[str, str, str, str], ...]) -> int:
    extra_energy, amphipod_count = 0, defaultdict(int)

    # Build room tuples, stripping out any amphipods who are already in place.
    # Also calculate extra energy required as amphipods leave their starting rooms...
    room_occupants = defaultdict(list)
    for amphipods in amphipod_rows:
        for room_index, amphipod in enumerate(amphipods):
            room_occupants[room_index].append(ord(amphipod) - 65)
    for room_index, occupants in room_occupants.items():
        while occupants and occupants[-1] == room_index:
            occupants.pop()
        for position_in_room, amphipod in enumerate(occupants):
            amphipod_count[amphipod] += 1
            extra_energy += position_in_room * 10**amphipod

    # ...and add extra energy required for amphipods arriving at their destination
    for variant, count in amphipod_count.items():
        extra_energy += {1: 0, 2: 1, 3: 3, 4: 6}[count] * 10**variant

    rooms = tuple(tuple(occupants) for occupants in room_occupants.values())

    # Calculate initial estimate of 'cost to complete' (assume everybody moves directly)
    cost_to_complete = 0
    for i, occupants in enumerate(rooms):
        cost_to_complete += sum(
            (abs((a + 1) * 2 - ((i + 1) * 2)) + 2) * 10**a for a in occupants
        )

    hallway = tuple(None for _ in range(11))
    initial_state = (0, cost_to_complete, rooms, hallway)
    to_visit = [(cost_to_complete, id(initial_state), initial_state)]

    while to_visit:
        _, _, current_state = heappop(to_visit)
        if current_state[1] == 0:
            return current_state[0] + extra_energy
        for state in possible_next_states(current_state):
            # Heap ranks states by total cost - to date and estimated to complete
            # (plus the unqique id of the state as a tie-breaker)
            heappush(to_visit, (state[0] + state[1], id(state), state))

    return None


EXTRA_ROWS = (("D", "C", "B", "A"), ("D", "B", "A", "C"))


def solve(inputs):
    amphipod_data = inputs.splitlines()
    first_row = tuple(re.findall(r"[ABCD]", amphipod_data[2]))
    last_row = tuple(re.findall(r"[ABCD]", amphipod_data[3]))

    print(f"Part 1: {organise_amphipods((first_row, last_row))}")
    print(f"Part 2: {organise_amphipods( (first_row, *EXTRA_ROWS, last_row))}\n")


solve(sample_input)
solve(actual_input)
