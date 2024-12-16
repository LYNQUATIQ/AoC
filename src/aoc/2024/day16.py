"""https://adventofcode.com/2024/day/16"""

from collections import deque
from functools import cache
from heapq import heappop, heappush

from numpy import short

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 16)


example_input = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

NORTH, SOUTH, EAST, WEST = (0, -1), (0, 1), (1, 0), (-1, 0)
TURN_LEFT = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
TURN_RIGHT = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}

WALL, START, END = "#", "S", "E"


def solve(inputs: str):

    walls = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, char in enumerate(line):
            xy = (x, y)
            if char == START:
                start_tile = xy
            elif char == END:
                end_tile = xy
            elif char == WALL:
                walls.add(xy)

    @cache
    def distance_to_end(xy, facing):
        y_distance = abs(end_tile[1] - xy[1])
        x_distance = abs(end_tile[0] - xy[0])
        distance = x_distance + y_distance
        if facing in (NORTH, SOUTH) and x_distance > 0:
            distance += 1000
        if facing in (EAST, WEST) and y_distance > 0:
            distance += 1000
        return distance

    @cache
    def possible_steps(xy, facing):
        next_steps = [
            ((xy, TURN_LEFT[facing]), 1000),
            ((xy, TURN_RIGHT[facing]), 1000),
        ]
        next_xy = (xy[0] + facing[0], xy[1] + facing[1])
        if next_xy not in walls:
            next_steps.append(((next_xy, facing), 1))
        return next_steps

    def shortest_path(start: complex, facing: complex) -> int:
        visited: set[(complex, complex)] = set()
        distance_to = {(start, facing): 0}
        to_visit: list[tuple[float, (complex, complex)]] = []
        heappush(to_visit, (distance_to_end(start, facing), (start, facing)))
        while to_visit:
            _, this_state = heappop(to_visit)
            xy, facing = this_state
            if xy == end_tile:
                return distance_to[this_state]
            visited.add(this_state)
            for next_state, step_cost in possible_steps(*this_state):
                distance_to_here = distance_to[this_state] + step_cost
                prior_distance_to_here = distance_to.get(next_state, 0)
                if next_state in visited and distance_to_here >= prior_distance_to_here:
                    continue
                if distance_to_here < prior_distance_to_here or next_state not in [
                    i[1] for i in to_visit
                ]:
                    distance_to[next_state] = distance_to_here
                    f_score = distance_to_here + distance_to_end(*next_state)
                    heappush(to_visit, (f_score, next_state))
        raise ValueError("No path found")

    print(f"Part 1: {int(shortest_path(start_tile, EAST))}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
