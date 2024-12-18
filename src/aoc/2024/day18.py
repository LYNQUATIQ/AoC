"""https://adventofcode.com/2024/day/18"""

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
        return [
            (xy[0] + d[0], xy[1] + d[1])
            for d in DIRECTIONS
            if (xy not in blocks) and (0 <= xy[0] <= extent) and (0 <= xy[1] <= extent)
        ]

    def distance_to_target(xy: Xy) -> int:
        return abs(target[0] - xy[0]) + abs(target[1] - xy[1])

    def shortest_path(blocks):
        visited: set[Xy] = set()
        distance_to = {start: 0}
        to_visit: list[tuple[float, Xy, list[Xy]]] = []
        heappush(to_visit, (distance_to_target(start), start))
        while to_visit:
            _, xy = heappop(to_visit)
            if xy == target:
                return distance_to[xy]
            visited.add(xy)
            for next_xy in possible_steps(xy, blocks):
                distance = distance_to[xy] + 1
                prior_best = distance_to.get(next_xy, 0)
                if next_xy in visited and distance >= prior_best:
                    continue
                if distance < prior_best or next_xy not in [i[1] for i in to_visit]:
                    distance_to[next_xy] = distance
                    f_score = distance + distance_to_target(next_xy)
                    heappush(to_visit, (f_score, next_xy))
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

    bad_block = falling_blocks[bad_delay - 1]
    print(f"Part 2: {bad_block[0]},{bad_block[1]}\n")


solve(example_input, 6, 12)
solve(actual_input, 70, 1024)
