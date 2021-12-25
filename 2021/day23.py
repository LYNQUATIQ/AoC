"""https://adventofcode.com/2021/day/23"""
import logging
import os

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day23.log")
# logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w", force=True)

from heapq import heappush, heappop
import re

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import TypeAlias

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day23_input.txt")) as f:
    actual_input = f.read()


sample_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
# sample_input = """#############
# #...........#
# ###B#A#C#D###
#   #A#B#C#D#
#   #########"""

EXTRA_ROWS = (("D", "C", "B", "A"), ("D", "B", "A", "C"))


AMBER, BRONZE, COPPER, DESERT = "A", "B", "C", "D"

# Rooms
AMBER_ROOM = "Amber room"
BRONZE_ROOM = "Bronze room"
COPPER_ROOM = "Copper room"
DESERT_ROOM = "Desert room"


AMPHIPOD_ROOM = {
    AMBER: AMBER_ROOM,
    BRONZE: BRONZE_ROOM,
    COPPER: COPPER_ROOM,
    DESERT: DESERT_ROOM,
}

# Hallways
L_FAR = "Left room far"
L_NEAR = "Left room near"
AB = "Hall between A/B"
BC = "Hall between B/C"
CD = "Hall between C/D"
R_NEAR = "Right room near"
R_FAR = "Right room far"

ROOMS = (AMBER_ROOM, BRONZE_ROOM, COPPER_ROOM, DESERT_ROOM)
HALLWAYS = (L_NEAR, R_NEAR, BC, AB, CD, L_FAR, R_FAR)

BETWEEN = {
    AMBER_ROOM: {
        L_FAR: {L_NEAR},
        L_NEAR: {},
        AB: {},
        BC: {AB},
        CD: {AB, BC},
        R_NEAR: {AB, BC, CD},
        R_FAR: {AB, BC, CD, R_NEAR},
    },
    BRONZE_ROOM: {
        L_FAR: {L_NEAR, AB},
        L_NEAR: {AB},
        AB: {},
        BC: {},
        CD: {BC},
        R_NEAR: {BC, CD},
        R_FAR: {BC, CD, R_NEAR},
    },
    COPPER_ROOM: {
        L_FAR: {L_NEAR, AB, BC},
        L_NEAR: {AB, BC},
        AB: {BC},
        BC: {},
        CD: {},
        R_NEAR: {CD},
        R_FAR: {CD, R_NEAR},
    },
    DESERT_ROOM: {
        L_FAR: {L_NEAR, AB, BC, CD},
        L_NEAR: {AB, BC, CD},
        AB: {BC, CD},
        BC: {CD},
        CD: {},
        R_NEAR: {},
        R_FAR: {R_NEAR},
    },
}

# Distances (as measured from first position in the room)
DISTANCES = {
    AMBER_ROOM: {
        L_FAR: 3,
        L_NEAR: 2,
        AB: 2,
        BC: 4,
        CD: 6,
        R_NEAR: 8,
        R_FAR: 9,
        AMBER_ROOM: 4,
        BRONZE_ROOM: 4,
        COPPER_ROOM: 6,
        DESERT_ROOM: 8,
    },
    BRONZE_ROOM: {
        L_FAR: 5,
        L_NEAR: 4,
        AB: 2,
        BC: 2,
        CD: 4,
        R_NEAR: 6,
        R_FAR: 7,
        AMBER_ROOM: 4,
        BRONZE_ROOM: 4,
        COPPER_ROOM: 4,
        DESERT_ROOM: 6,
    },
    COPPER_ROOM: {
        L_FAR: 7,
        L_NEAR: 6,
        AB: 4,
        BC: 2,
        CD: 2,
        R_NEAR: 4,
        R_FAR: 5,
        AMBER_ROOM: 6,
        BRONZE_ROOM: 4,
        COPPER_ROOM: 4,
        DESERT_ROOM: 4,
    },
    DESERT_ROOM: {
        L_FAR: 9,
        L_NEAR: 8,
        AB: 6,
        BC: 4,
        CD: 2,
        R_NEAR: 2,
        R_FAR: 3,
        AMBER_ROOM: 8,
        BRONZE_ROOM: 6,
        COPPER_ROOM: 4,
        DESERT_ROOM: 4,
    },
}

ENERGY = {AMBER: 1, BRONZE: 10, COPPER: 100, DESERT: 1000}

MAX_MOVES = 2

Room: TypeAlias = str
RoomPosition: TypeAlias = int
Hallway: TypeAlias = str
AmphipodVariant: TypeAlias = str  # 'A', 'B', 'C' or 'D'


@dataclass(frozen=True, order=True)
class Amphipod:
    variant: AmphipodVariant
    index: int

    def __repr__(self) -> str:
        return f"{self.variant}{self.index}"


RoomLists: TypeAlias = tuple[tuple[Room, tuple[Amphipod]]]
Move: TypeAlias = tuple[Amphipod, Room | Hallway, Hallway | Room]
AmphipodPositions: TypeAlias = tuple[tuple[Amphipod, Room, int], ...]
AmphipodState: TypeAlias = tuple[AmphipodPositions, tuple[Move, ...], int]


@lru_cache(maxsize=None)
def possible_moves(amphipod_positions: AmphipodPositions) -> list[Move]:
    amphipods_in_hallway = {h: a for a, h, _ in amphipod_positions if h in HALLWAYS}
    amphipods_in_rooms = {
        r: a for a, r, i in amphipod_positions if r in ROOMS and i == 0
    }
    moves = []
    for amphipod, start, posititon in amphipod_positions:
        if start in HALLWAYS:
            destination = AMPHIPOD_ROOM[amphipod.variant]
            if amphipods_in_rooms.get(destination, False):
                continue  # There's somebody in the room who still needs to move
            if any(h in amphipods_in_hallway for h in BETWEEN[destination][start]):
                continue  # There's somebody blocking the hallway between here and room
            moves.append((amphipod, start, destination))
        else:
            if posititon != 0:
                continue
            for destination in HALLWAYS:
                if destination in amphipods_in_hallway:
                    continue  # There's somebody already there
                if any(h in amphipods_in_hallway for h in BETWEEN[start][destination]):
                    continue  # There's somebody blocking the way en route to hallway
                moves.append((amphipod, start, destination))
    return moves


@lru_cache(maxsize=None)
def update_state(state: AmphipodState, move: Move) -> AmphipodState:
    amphipod_positions, moves, energy_so_far = state
    amphipod, start, destination = move

    if destination in HALLWAYS:
        updated_amphipod_positions = (
            (
                a,
                destination if a == amphipod else r,
                (p - 1) if r == start and a != amphipod else p,
            )
            for a, r, p in amphipod_positions
        )
    else:
        updated_amphipod_positions = (
            (a, r, p) for a, r, p in amphipod_positions if a != amphipod
        )
    energy_for_move = energy_required_for_move(move)
    return (
        tuple(updated_amphipod_positions),
        (*moves, (amphipod, destination, energy_for_move)),
        energy_so_far + energy_for_move,
    )


def energy_to_complete(amphipods: AmphipodPositions) -> int:
    return sum(
        DISTANCES[AMPHIPOD_ROOM[a.variant]][r] * ENERGY[a.variant]
        for a, r, _ in amphipods
    )


def energy_required_for_move(move: Move) -> int:
    amphipod, start, destination = move
    room, hallway = (start, destination) if start in ROOMS else (destination, start)
    return DISTANCES[room][hallway] * ENERGY[amphipod.variant]


def organise_amphipods(starting_room_lists: RoomLists) -> int:

    energy = 0
    variant_count = defaultdict(int)
    amphipod_positions = []

    # Strip out any amphipods who are already in place.
    # Also adjust the energy for the initial moves as amphipods leave.
    for room, room_tuple in starting_room_lists:
        room_list = list(room_tuple)
        while room_list and AMPHIPOD_ROOM[room_list[-1].variant] == room:
            room_list.pop()
        for position_in_room, amphipod in enumerate(room_list):
            amphipod_positions.append((amphipod, room, position_in_room))
            variant_count[amphipod.variant] += 1
            energy += ENERGY[amphipod.variant] * position_in_room

    # Adjust energy for them arriving at their destination
    for variant, count in variant_count.items():
        energy += ENERGY[variant] * {1: 0, 2: 1, 3: 3, 4: 6}[count]

    initial_state: AmphipodState = (tuple(amphipod_positions), (), energy)
    to_visit = [(0, initial_state)]
    while to_visit:
        _, state = heappop(to_visit)
        amphipod_positions, moves, energy_so_far = state
        if not amphipod_positions:
            print(moves)
            return energy_so_far

        for move in possible_moves(amphipod_positions):
            updated_state = update_state(state, move)
            next_positions, _, energy_to_get_here = state
            heap_cost = energy_to_get_here + energy_to_complete(next_positions)
            heappush(to_visit, (heap_cost, updated_state))

    return None


@print_time_taken
def solve(inputs):

    amphipod_data = inputs.splitlines()
    top_row = tuple(re.findall(r"[ABCD]", amphipod_data[2]))
    bottom_row = tuple(re.findall(r"[ABCD]", amphipod_data[3]))

    def get_starting_room_lists(rows) -> RoomLists:
        starting_room_lists, amphipod_counter = defaultdict(list), defaultdict(int)
        for amphipods in rows:
            for room, a in zip(ROOMS, amphipods):
                amphipod_counter[a] += 1
                starting_room_lists[room].append(Amphipod(a, amphipod_counter[a]))
        return tuple(
            (room, tuple(occupants)) for room, occupants in starting_room_lists.items()
        )

    starting_room_lists = get_starting_room_lists((top_row, bottom_row))
    print(f"Part 1: {organise_amphipods(starting_room_lists)}")

    starting_room_lists = get_starting_room_lists((top_row, *EXTRA_ROWS, bottom_row))
    print(f"Part 2: {organise_amphipods(starting_room_lists)}\n")


solve(sample_input)
solve(actual_input)
