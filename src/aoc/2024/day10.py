"""https://adventofcode.com/2024/day/10"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 10)


example_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

example_input = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""

NORTH = -1j
SOUTH = 1j
EAST = 1
WEST = -1


def solve(inputs: str):
    grid = {}
    trailheads = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, cell in enumerate(row):
            xy = complex(x, y)
            grid[xy] = -1 if cell == "." else int(cell)
            if cell == "0":
                trailheads.add(xy)

    score = 0
    for trailhead in trailheads:
        visited = set()
        to_visit = {trailhead}
        while to_visit:
            xy = to_visit.pop()
            visited.add(xy)
            value = grid[xy]
            if value == 9:
                score += 1
                continue
            for neighbour in [xy + d for d in (NORTH, SOUTH, EAST, WEST)]:
                if grid.get(neighbour) == value + 1 and (neighbour not in visited):
                    to_visit.add(neighbour)

    print(f"Part 1: {score}")

    total_rating = 0
    for trailhead in trailheads:
        visited = set()
        to_visit = {(trailhead, ())}
        while to_visit:
            xy, route_here = to_visit.pop()
            route_here = tuple([xy] + list(route_here))
            visited.add((xy, route_here))
            value = grid[xy]
            if value == 9:
                total_rating += 1
                continue
            for neighbour in [xy + d for d in (NORTH, SOUTH, EAST, WEST)]:
                if grid.get(neighbour) == value + 1:
                    to_visit.add((neighbour, route_here))

    print(f"Part 2: {total_rating}\n")


solve(example_input)
solve(actual_input)
