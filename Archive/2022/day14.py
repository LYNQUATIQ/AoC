"""https://adventofcode.com/2022/day/14"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day14_input.txt")) as f:
    actual_input = f.read()


sample_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

SAND_SOURCE = (500, 0)


def solve(inputs: str) -> None:
    blocked = set()
    for line in inputs.splitlines():
        points = [tuple(map(int, p.split(","))) for p in line.split(" -> ")]
        for (start_x, start_y), (end_x, end_y) in zip(points[:-1], points[1:]):
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                    blocked.add((x, y))

    max_y, number_of_rocks = max(xy[1] for xy in blocked), len(blocked)
    cavern_floor = max_y + 2
    part_1 = None
    sand_sources = [SAND_SOURCE]
    while True:
        x, y = sand_sources.pop()

        # Fall until blocked
        while next_xy := [
            xy
            for xy in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1))
            if xy not in blocked and xy[1] != cavern_floor
        ]:
            sand_sources.append((x, y))
            x, y = next_xy[0]

        if not part_1 and y > max_y:
            part_1 = len(blocked) - number_of_rocks

        blocked.add((x, y))
        if (x, y) == SAND_SOURCE:
            break

    print(f"Part 1: {part_1}")
    print(f"Part 2: {len(blocked) - number_of_rocks}\n")


solve(sample_input)
solve(actual_input)
