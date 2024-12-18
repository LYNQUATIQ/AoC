"""https://adventofcode.com/2024/day/18"""

from functools import cache
from heapq import heappop, heappush

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 18)


example_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

Xy = tuple[int, int]

NORTH, SOUTH, EAST, WEST = (0, -1), (0, 1), (1, 0), (-1, 0)
DIRECTIONS = (NORTH, SOUTH, EAST, WEST)


def solve(inputs: str, extent: int, initial_delay: int):
    falling_blocks = []
    for line in inputs.splitlines():
        falling_blocks.append(tuple(map(int, line.split(","))))

    start = (0, 0)
    target = (extent, extent)

    def possible_steps(xy: Xy, blocks: set[Xy]) -> list[Xy]:
        possible_steps = [(xy[0] + d[0], xy[1] + d[1]) for d in DIRECTIONS]
        possible_steps = [xy for xy in possible_steps if xy not in blocks]
        return [
            xy
            for xy in possible_steps
            if (0 <= xy[0] <= extent) and (0 <= xy[1] <= extent)
        ]

    def draw_map(extent, blocks, path=set()):
        for y in range(extent + 1):
            for x in range(extent + 1):
                c = "#" if (x, y) in blocks else "."
                c = "O" if (x, y) in path else c
                print(c, end="")
            print()

    def shortest_path(blocks):
        visited: set[Xy] = set()
        distance_to = {start: 0}
        path_to = {start: []}
        to_visit: list[tuple[float, Xy, list[Xy]]] = []
        heappush(to_visit, (extent * 2, start))
        while to_visit:
            _, this_state = heappop(to_visit)
            xy = this_state
            if xy == target:
                return distance_to[this_state]
            visited.add(this_state)
            for next_state in possible_steps(xy, blocks):
                distance = distance_to[this_state] + 1
                prior_distance = distance_to.get(next_state, 0)
                if next_state in visited and distance >= prior_distance:
                    continue
                if distance < prior_distance or next_state not in [
                    i[1] for i in to_visit
                ]:
                    distance_to[next_state] = distance
                    path_to[next_state] = path_to[this_state] + [next_state]
                    f_score = (
                        distance
                        + abs(target[0] - next_state[0])
                        + abs(target[1] - next_state[1])
                    )
                    heappush(to_visit, (f_score, next_state))

        raise ValueError("No path found")

    print(f"Part 1: {shortest_path(set(falling_blocks[:initial_delay]))}")

    good_delay = initial_delay
    bad_delay = len(falling_blocks) + 1
    while bad_delay != (good_delay + 1):
        next_delay = good_delay + ((bad_delay - good_delay) // 2)
        try:
            shortest_path(set(falling_blocks[:next_delay]))
            good_delay = next_delay
        except ValueError:
            bad_delay = next_delay

    bad_block = falling_blocks[bad_delay]
    print(f"Part 2: {bad_block[0]},{bad_block[1]}\n")


solve(example_input, 6, 12)
solve(actual_input, 70, 1024)
# 250 too low
