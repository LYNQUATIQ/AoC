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


NORTH = -1j
SOUTH = 1j
EAST = 1
WEST = -1


def walk_trails(
    grid: dict[complex, int], trailheads: set[complex], compute_rating: bool = False
) -> int:
    score = 0
    for trailhead in trailheads:
        visited = set()
        to_visit = {(trailhead, ())}
        while to_visit:
            xy, route_here = to_visit.pop()
            if compute_rating:
                route_here = tuple([xy] + list(route_here))
            visited.add((xy, route_here))
            value = grid[xy]
            if value == 9:
                score += 1
                continue
            for neighbour in [xy + d for d in (NORTH, SOUTH, EAST, WEST)]:
                if grid.get(neighbour) == value + 1:
                    if (neighbour, route_here) not in visited:
                        to_visit.add((neighbour, route_here))
    return score


def solve(inputs: str):
    grid, trailheads = {}, set()
    for y, row in enumerate(inputs.splitlines()):
        for x, cell in enumerate(row):
            xy = complex(x, y)
            grid[xy] = int(cell)
            if cell == "0":
                trailheads.add(xy)

    print(f"Part 1: {walk_trails(grid, trailheads)}")
    print(f"Part 2: {walk_trails(grid, trailheads, compute_rating=True)}\n")


solve(example_input)
solve(actual_input)
