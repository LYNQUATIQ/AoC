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
NSEW = (NORTH, SOUTH, EAST, WEST)


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

    # Determine the steps on the route and the time taken to get to each step
    xy, step, route = start, 0, {start: 0}
    possible_headings = [d for d in NSEW if xy + d not in walls]
    while heading := (possible_headings[0] if possible_headings else None):
        route[(xy := xy + heading)] = (step := step + 1)
        possible_headings = [d for d in NSEW if xy + d not in walls and d != -heading]
    assert xy == end

    def get_cheat_count(rule_time: int) -> dict[int, int]:
        cheat_count = defaultdict(int)
        for route_step, cheat_start_time in route.items():
            candidate_cheats, visited, to_visit = {}, set(), {route_step}
            for time_taken in range(1, rule_time + 1):
                next_to_visit = set()
                for xy in to_visit:
                    visited.add(xy)
                    for next_xy in [xy + d for d in NSEW if xy + d not in visited]:
                        next_to_visit.add(next_xy)
                        if next_xy in route:
                            time_saved = route[next_xy] - cheat_start_time - time_taken
                            if time_saved > 0:
                                candidate_cheats[next_xy] = time_saved
                to_visit = next_to_visit
            for time_saved in candidate_cheats.values():
                cheat_count[time_saved] += 1
        return cheat_count

    cheat_count = get_cheat_count(rule_time=2)
    cheat_over_100 = sum(count for gain, count in cheat_count.items() if gain >= 100)
    print(f"Part 1: {cheat_over_100}")

    cheat_count = get_cheat_count(rule_time=20)
    cheat_over_100 = sum(count for gain, count in cheat_count.items() if gain >= 100)
    print(f"Part 2: {cheat_over_100}\n")


solve(example_input)
solve(actual_input)
