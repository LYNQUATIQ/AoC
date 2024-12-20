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


def solve(inputs: str):
    walls, start, end = set(), None, None
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            xy = complex(x, y)
            if c == WALL:
                walls.add(xy)
            elif c == START:
                start = xy
            elif c == END:
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
        except KeyError:  # Reached a dead end (i.e. the end)
            break
    assert xy == end

    def get_cheat_count(rule_time: int) -> dict[int, int]:
        cheat_count = defaultdict(int)
        for step_xy, step in route.items():
            candidate_cheats = {}
            to_visit, visited = {step_xy}, set()
            for time_taken in range(rule_time):
                next_to_visit = set()
                for xy in to_visit:
                    visited.add(xy)
                    for next_xy in [xy + d for d in DIRECTIONS if xy + d]:
                        if next_xy in visited or next_xy in candidate_cheats:
                            continue
                        next_to_visit.add(next_xy)
                        if next_xy in route:
                            cheat_gain = route[next_xy] - step - (time_taken + 1)
                            if cheat_gain > 0:
                                candidate_cheats[next_xy] = cheat_gain
                to_visit = next_to_visit
            for cheat_gain in candidate_cheats.values():
                cheat_count[cheat_gain] += 1
        return cheat_count

    cheat_count = get_cheat_count(rule_time=2)
    cheat_over_100 = sum(count for gain, count in cheat_count.items() if gain >= 100)
    print(f"Part 1: {cheat_over_100}")

    cheat_count = get_cheat_count(rule_time=20)
    cheat_over_100 = sum(count for gain, count in cheat_count.items() if gain >= 100)
    print(f"Part 2: {cheat_over_100}\n")


solve(example_input)
solve(actual_input)
