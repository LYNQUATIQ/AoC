"""https://adventofcode.com/2022/day/14"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()


sample_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

SAND_SOURCE = (500, 0)


def solve(inputs: str) -> None:
    blocked = set()
    for line in inputs.splitlines():
        points = [tuple(map(int, p.split(","))) for p in line.split(" -> ")]
        for (start_x, start_y), (end_x, end_y) in zip(points[:-1], points[1:]):
            if start_x == end_x:
                s = 1 if end_y > start_y else -1
                blocked |= {(end_x, y) for y in range(start_y, end_y + s, s)}
            else:
                s = 1 if end_x > start_x else -1
                blocked |= {(x, end_y) for x in range(start_x, end_x + s, s)}

    cavern_floor, number_of_rocks = max(xy[1] for xy in blocked) + 2, len(blocked)
    part_1 = None
    sand_sources = [SAND_SOURCE]
    while True:
        current_source = sand_sources.pop()
        x, y = last_source = current_source

        # Fall until blocked
        while space_below := [
            (next_x, next_y)
            for next_x, next_y in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1))
            if (next_x, next_y) not in blocked and next_y != cavern_floor
        ]:
            sand_sources.append(last_source)
            last_source = x, y
            x, y = space_below[0]

        if not part_1 and y > cavern_floor - 2:
            part_1 = len(blocked) - number_of_rocks

        blocked.add((x, y))
        if (x, y) == SAND_SOURCE:
            break

    print(f"Part 1: {part_1}")
    print(f"Part 2: {len(blocked) - number_of_rocks}\n")


solve(sample_input)
solve(actual_input)
