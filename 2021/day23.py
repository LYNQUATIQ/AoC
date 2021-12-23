"""https://adventofcode.com/2021/day/23

Each move, if anybody not done:

- If there's a D not done can I move them to room 4 - check for complete?
- If there's a C not done can I move them to room 3 - check for complete?
- If there's a B not done can I move them to room 2 - check for complete?
- If there's a A not done can I move them to room 1 - check for complete?


D - 12
C - 4
B - 9 + 2
A - 9 + 2

6 routes:
Move straight to destination - takes known steps (+1 for first in)
Move out, stop in one of three middle hall spots, and then move in
Move out, stop in left hall far spot, and then move in
Move out, stop in left hall near spot, and then move in
Move out, stop in right hall far spot, and then move in
Move out, stop in right hall near spot, and then move in
(First into room must take 1 extra step)

5 empty rooms - 2 can fit two people, 3 can fit 1
3 small ones block others moving 
Rooms have far and near spots:
For destinations, first one in takes an extra move to get to far spot
When leaving, second one out takes extra move to get to the door
If entering side room and someone there +2 to them as they would have to moved to back

Route for D's is always going to be from their current room staight to target
Minimise people moving past/away from their room - first A then B then C 
Rooms are LIFO queues

At any moment I have a priority...
- Unblock back of room 4 if necessary
    - Unblock front or room 4 if necessary
    
Search is move everybody up to 'n' (2 in part 1) legal steps and take cheapest solution.
On a move I can move to any empty room that has space:


D can never stop in halls/end rooms (except to unblock D)
C can stop to let D past


Anyone 'not in place' (upto 8)...
Can only move if:
    In front of room if my room not blocked or 'good' space in hall
    In back of room and front empty and my room not blocked or 'good' space in hall
    In hall/L/R as long as my room not blocked

Blocked rooms are rooms with wrong variant in.
Must 'unblock' rooms

Bad scenario...
Someone in hall AND not enough open hall spaces on destination side for
blockers in their destination
for everybody who ???

4 LIFO Room Queues?

Will never move into an amphipod room other than your own.
When moving into your room you always go as far in as you can.
Can move into side rooms - can fit upto two people (LIFO)... don't worry about which
space you move into... assume it's door if your the only one using it... oherwise if
somebody else uses it after you, assume you went to the back.

Model as 6 *rooms*... all LIFO with room for 2 (or 4 in part 2).
Plus 3 stopping points between A/B, B/C and C/D.
Your first move is either to a stopping point, one of the side rooms, or *your* room
(only if it's empty).

Everybody makes 1 move to the hall or a L/R right, and then movees to their room.
Sombody may make make both their moves before somebody else starts. 

Only amphipods who can move are:
1) the ones at the front of each queue in each room closest to the door
2) the (upto) seven in the hallway provided they can get in their room and they're not
   blocked inbetween
   
Track 'unresolved' amphipods, i.e. amphipods not in their rooms or who are in their room
but need to move out and back in to let somebody else outself.
Everybody makes exactly 0 or 2 moves.
Amphipod state is either:
   - DONE (in their room with no dodgy neighbours) - moved 2 (or maybe 0) times
   - BLOCKED_IN_ROOM (haven't moved yet and can't get out to the hallway) - moved 0
   - IN_PLAY_IN_ROOM (can move out of the room and into the hallway) - moved 0
   - BLOCKED_IN_HALL (can't move to their room because hallway/room is blocked) - moved 1
   - IN_PLAY_IN_HALL (able to move to their room and become DONE) - moved 1
N.B. Ignore anybody who starts 'DONE' altogether ==> *everybody* makes two moves...
     Once to the hall and once to their room
     Everybody in a room must move to a hallway space.
     Everybody in the hall must make one move to their room.

    So unresolved/remaining amphipods have only two states:
       TO_MOVE_TO_HALL (move to 1 of 7 spaces)
       TO_MOVE_HOME
To model game:
   - Note everybody's starting position (room and place in room)
   
Game state:
Everybody's current position (1 of the 11 rooms/hallway spaces)
N.B. Room is blocked if there is anybody in it of wrong variant
"""
import logging
import os

log_file = os.path.join(os.path.dirname(__file__), f"logs/day23.log")
logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w", force=True)

import math
import re
import string
import sys

from collections import defaultdict, Counter
from dataclasses import dataclass, field
from functools import cache
from itertools import chain, product
from typing import Hashable, TypeAlias

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

# Rooms
AMBER_ROOM = "Amber room"
BRONZE_ROOM = "Bronze room"
COPPER_ROOM = "Copper room"
DESERT_ROOM = "Desert room"

# Hallways
LEFT_FAR = "Left room far"
LEFT_NEAR = "Left room near"
HALL_AB = "Hall between A/B"
HALL_BC = "Hall between B/C"
HALL_CD = "Hall between C/D"
RIGHT_NEAR = "Right room near"
RIGHT_FAR = "Right room far"

ROOMS = (AMBER_ROOM, BRONZE_ROOM, COPPER_ROOM, DESERT_ROOM)
HALLWAY = (LEFT_FAR, LEFT_NEAR, HALL_AB, HALL_BC, HALL_CD, RIGHT_NEAR, RIGHT_FAR)

BETWEEN = {
    AMBER_ROOM: {
        LEFT_FAR: {LEFT_NEAR},
        LEFT_NEAR: {},
        HALL_AB: {},
        HALL_BC: {HALL_AB},
        HALL_CD: {HALL_AB, HALL_BC},
        RIGHT_NEAR: {HALL_AB, HALL_BC, HALL_CD},
        RIGHT_FAR: {HALL_AB, HALL_BC, HALL_CD, RIGHT_NEAR},
    },
    BRONZE_ROOM: {
        LEFT_FAR: {LEFT_NEAR, HALL_AB},
        LEFT_NEAR: {HALL_AB},
        HALL_AB: {},
        HALL_BC: {},
        HALL_CD: {HALL_BC},
        RIGHT_NEAR: {HALL_BC, HALL_CD},
        RIGHT_FAR: {HALL_BC, HALL_CD, RIGHT_NEAR},
    },
    COPPER_ROOM: {
        LEFT_FAR: {LEFT_NEAR, HALL_AB, HALL_BC},
        LEFT_NEAR: {HALL_AB, HALL_BC},
        HALL_AB: {HALL_BC},
        HALL_BC: {},
        HALL_CD: {},
        RIGHT_NEAR: {HALL_CD},
        RIGHT_FAR: {HALL_CD, RIGHT_NEAR},
    },
    DESERT_ROOM: {
        LEFT_FAR: {LEFT_NEAR, HALL_AB, HALL_BC, HALL_CD},
        LEFT_NEAR: {HALL_AB, HALL_BC, HALL_CD},
        HALL_AB: {HALL_BC, HALL_CD},
        HALL_BC: {HALL_CD},
        HALL_CD: {},
        RIGHT_NEAR: {},
        RIGHT_FAR: {HALL_CD, RIGHT_NEAR},
    },
}


AMBER, BRONZE, COPPER, DESERT = "A", "B", "C", "D"

AMPHIPOD_ROOM = {
    AMBER: AMBER_ROOM,
    BRONZE: BRONZE_ROOM,
    COPPER: COPPER_ROOM,
    DESERT: DESERT_ROOM,
}

ENERGY = {AMBER: 1, BRONZE: 10, COPPER: 100, DESERT: 1000}

MAX_MOVES = 2

Room: TypeAlias = str
AmphipodVariant: TypeAlias = str  # 'A', 'B', 'C' or 'D'


@dataclass(frozen=True)
class Amphipod:
    variant: AmphipodVariant
    index: int

    def __repr__(self) -> str:
        return f"{self.variant}{self.index}"


AmphipodState: TypeAlias = dict[Amphipod:Room]  # Just the ones not already 'done'


@cache
def possible_moves(position: Room, occupied: tuple[Room]) -> list[tuple[Room, int]]:
    """Return possible moves and distances from the current position (taking account of
    rooms you can't visit)"""
    possible_moves = []
    blocked = set(occupied)
    to_check = [(n, 1) for n in NEXT_STEPS[position]]
    while to_check:
        new_position, steps = to_check.pop()
        if new_position in blocked:
            continue
        if new_position not in CANNOT_STOP:
            possible_moves.append((new_position, steps))
        to_check.extend([(n, steps + 1) for n in NEXT_STEPS[new_position]])
        blocked.add(new_position)
    return possible_moves


@cache
def best_dance_from_here(
    dance_so_far: AmphipodDance, to_beat: int
) -> AmphipodDance | None:
    """Returns the best dance from here (or none if none of them beat best so far)"""

    energy_taken = sum(steps * ENERGY[a.variant] for a, _, steps in dance_so_far)
    if energy_taken > to_beat:
        return None

    # Gather info about current state - positions, # moves, energy required, etc.
    positions = {}
    moves_so_far = defaultdict(lambda: -1)
    for amphipod, position, _ in dance_so_far:
        positions[amphipod] = position
        moves_so_far[amphipod] += 1
    # energy_required = {}
    # in_back = {}
    # for a, position in positions.items():
    #     energy_required[a] = DISTANCES[a.variant][position] * ENERGY[a.variant]
    # for variant, room in TARGET_BACK_ROOM.items():
    #     if position == room:
    #         in_back[variant] = a

    # log_string = "".join(
    #     f"   {a.variant}{a.index} moves to {r}\n" for a, r, _ in dance_so_far[8:]
    # )
    # logging.warning(f"Looking for dances from\n{log_string}ENERGY:{energy_taken}\n")

    # If everybody in their target room we're done
    if all(position in AMPHIPOD_TARGET[a.variant] for a, position in positions.items()):
        return dance_so_far

    # Amphipods can move if they haven't moved twice (and their not in their back room)
    can_move = [
        a
        for a, steps in moves_so_far.items()
        if steps < MAX_MOVES and positions[a] != TARGET_BACK_ROOM[a.variant]
    ]

    # Explore possible next steps
    best_dance = None
    occupied = tuple(positions.values())
    next_dance_steps = []
    for amphipod in can_move:
        for next_step, distance in possible_moves(positions[amphipod], occupied):
            # Can't move to an amphipod room unless it's yours
            if (
                next_step in AMPHIPOD_ROOMS
                and next_step not in AMPHIPOD_TARGET[amphipod.variant]
            ):
                continue
            if moves_so_far[amphipod] == 1:
                # Can't move anywhere other than your room on second move
                if next_step not in AMPHIPOD_TARGET[amphipod.variant]:
                    continue
                # else:
                #     # Can't move to your room if your variant not in back (or empty)
                #     if (
                #         not in_back.get(amphipod.variant, amphipod.variant)
                #         == amphipod.variant
                #     ):
                #         continue
            v, p = amphipod.variant, positions[amphipod]
            energy_change = (DISTANCES[v][next_step] - DISTANCES[v][p]) * ENERGY[v]
            next_dance_steps.append((energy_change, (amphipod, next_step, distance)))

    for _, next_step in sorted(next_dance_steps, key=lambda x: x[0]):
        dance = best_dance_from_here((*dance_so_far, next_step), to_beat)
        if dance:
            energy_taken = sum(steps * ENERGY[a.variant] for a, _, steps in dance)
            if energy_taken < to_beat:
                best_dance, to_beat = dance, energy_taken
    return best_dance


def energy_to_organise(amphipods: AmphipodState) -> int:
    dance_so_far = tuple([(amphipod, room, 0) for amphipod, room in amphipods.items()])
    best_dance = best_dance_from_here(dance_so_far, 12522)  # sys.maxsize)
    if best_dance is None:
        return "no solution"
    return sum(steps * ENERGY[a.variant] for a, _, steps in best_dance)


@print_time_taken
def solve(inputs):
    amphipods = {}
    amphipod_counter = defaultdict(int)
    for i, line in enumerate(inputs.splitlines()):
        if i in (2, 3):
            for room, a in zip(AMPHIPOD_TARGET, list(re.findall(r"[ABCD]", line))):
                amphipod_counter[a] += 1
                amphipods[Amphipod(a, amphipod_counter[a])] = AMPHIPOD_TARGET[room][
                    i - 2
                ]

    print(f"Part 1: {energy_to_organise(amphipods)}")

    print(f"Part 2: {False}\n")


solve(sample_input)
# solve(actual_input)
