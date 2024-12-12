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
    width, height = x + 1, y + 1

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
        area = len(region)
        fencing = 4 * area
        for plant in region:
            for neighbour in [plant + d for d in [1, -1, 1j, -1j]]:
                if neighbour in region:
                    fencing -= 1
        total_cost += fencing * area
        # print(
        #     f" - A region of {grid[list(region)[0]]} plans with a price of {area} x {fencing} = {fencing * area}"
        # )
    print(f"Part 1: {total_cost}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
