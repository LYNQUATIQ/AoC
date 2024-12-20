"""https://adventofcode.com/2024/day/20"""

from collections import defaultdict
from aoc_utils import get_input_data

actual_input = get_input_data(2024, 20)


example_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

WALL, START, END = "#", "S", "E"
NORTH, SOUTH, EAST, WEST = -1j, 1j, 1, -1
DIRECTIONS = {NORTH, SOUTH, EAST, WEST}
LEFT_RIGHT = {
    NORTH: (WEST, EAST),
    EAST: (NORTH, SOUTH),
    SOUTH: (EAST, WEST),
    WEST: (SOUTH, NORTH),
}


def solve(inputs: str, verbose: bool = False):
    walls = set()
    start, end = None, None
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            xy = complex(x, y)
            if c == WALL:
                walls.add(xy)
            if c == START:
                start = xy
            if c == END:
                end = xy
    assert start is not None and end is not None

    xy, heading, step = start, NORTH, 0
    route = {start: 0}
    while True:
        xy += heading
        step += 1
        route[xy] = step
        walls_by_xy = {d for d in DIRECTIONS if xy + d in walls}
        try:
            heading = (DIRECTIONS - set(walls_by_xy) - {heading * -1}).pop()
        except KeyError:
            break

    def get_cheat_count(rule_time: int) -> dict[int, int]:
        cheat_count = defaultdict(int)
        for step_xy, step in route.items():
            candidate_cheats = {}
            to_visit = {step_xy}
            visited = set()
            time_taken = 1
            while time_taken <= rule_time:
                next_to_visit = set()
                for xy in to_visit:
                    visited.add(xy)
                    for next_xy in [
                        xy + d for d in DIRECTIONS if xy + d not in visited
                    ]:
                        next_to_visit.add(next_xy)
                        if next_xy not in route:
                            continue
                        cheat_gain = route[next_xy] - step - time_taken
                        if cheat_gain > 0 and next_xy not in candidate_cheats:
                            candidate_cheats[next_xy] = cheat_gain
                to_visit = next_to_visit
                time_taken += 1
            for cheat_gain in candidate_cheats.values():
                cheat_count[cheat_gain] += 1
        return cheat_count

    cheat_count = get_cheat_count(rule_time=2)
    if verbose:
        for gain, count in sorted(cheat_count.items()):
            print(f"There are {count} cheats that save {gain} picoseconds.")
    cheat_over_100 = sum(count for gain, count in cheat_count.items() if gain >= 100)
    print(f"Part 1: {cheat_over_100}")

    cheat_count = get_cheat_count(rule_time=20)
    if verbose:
        print()
        for gain, count in sorted(cheat_count.items()):
            if gain >= 50:
                print(f"There are {count} cheats that save {gain} picoseconds.")
    cheat_over_100 = sum(count for gain, count in cheat_count.items() if gain >= 100)
    print(f"Part 2: {cheat_over_100}\n")


solve(example_input, verbose=True)
solve(actual_input)
