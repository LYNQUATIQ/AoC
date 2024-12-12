"""https://adventofcode.com/2024/day/12"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 12)
example_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def solve(inputs: str):
    grid = {}
    for y, row in enumerate(inputs.splitlines()):
        for x, plant in enumerate(row):
            grid[complex(x, y)] = plant

    regions = []
    plants_to_check = set(grid.keys())
    while plants_to_check:
        xy = plants_to_check.pop()
        plant = grid[xy]
        region = {xy}
        to_visit = {xy}
        while to_visit:
            xy = to_visit.pop()
            for neighbour in [xy + d for d in [1, -1, 1j, -1j]]:
                if neighbour in region or grid.get(neighbour, "") != plant:
                    continue
                region.add(neighbour)
                to_visit.add(neighbour)
                plants_to_check.discard(neighbour)
        regions.append(region)

    total_cost = 0
    for region in regions:
        area, fencing = len(region), 0
        for plant in region:
            for neighbour in [plant + d for d in [1, -1, 1j, -1j]]:
                if neighbour not in region:
                    fencing += 1
        total_cost += fencing * area
    print(f"Part 1: {total_cost}")

    total_cost = 0
    for region in regions:
        if grid[list(region)[0]] == "M":
            pass
        area, sides = len(region), set()
        for plant in region:
            for direction in [1, -1, 1j, -1j]:
                if plant + direction not in region:
                    sides.add((plant, direction))
        n_sides, sides_to_check = 0, sides.copy()
        while sides_to_check:
            n_sides += 1
            xy, side = sides_to_check.pop()
            left_direction, right_direction = {
                1: [-1j, 1j],
                -1: [-1j, 1j],
                1j: [-1, 1],
                -1j: [-1, 1],
            }[side]
            lhs, rhs = xy + left_direction, xy + right_direction
            while lhs in region:
                try:
                    sides_to_check.remove((lhs, side))
                except KeyError:
                    break
                lhs += left_direction
            while rhs in region:
                try:
                    sides_to_check.remove((rhs, side))
                except KeyError:
                    break
                rhs += right_direction
        total_cost += n_sides * area

    print(f"Part 2: {total_cost}\n")


solve(example_input)
solve(actual_input)
