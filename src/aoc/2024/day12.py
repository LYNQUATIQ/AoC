"""https://adventofcode.com/2024/day/12"""

from itertools import product

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

NORTH, EAST, SOUTH, WEST = -1j, 1, 1j, -1
DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
LEFT_RIGHT = {
    NORTH: (WEST, EAST),
    EAST: (NORTH, SOUTH),
    SOUTH: (EAST, WEST),
    WEST: (SOUTH, NORTH),
}


def solve(inputs: str):
    plots: dict[complex, str] = {}
    for y, row in enumerate(inputs.splitlines()):
        for x, plant in enumerate(row):
            plots[complex(x, y)] = plant

    regions: list[set[complex]] = []
    plots_to_check = set(plots.keys())
    while plots_to_check:
        plot = plots_to_check.pop()
        region, regional_plant = {plot}, plots[plot]
        to_visit = {plot}
        while to_visit:
            plot = to_visit.pop()
            for neighbour in [plot + d for d in DIRECTIONS]:
                if neighbour in plots_to_check:
                    if plots.get(neighbour) == regional_plant:
                        region.add(neighbour)
                        plots_to_check.discard(neighbour)
                        to_visit.add(neighbour)
        regions.append(region)

    total_cost_part_1 = 0
    total_cost_part_2 = 0
    for region in regions:
        area = len(region)

        # Find all the fence panels that separate plots in this region from other
        # regions (noting both the plot position and in which direction the fence is)
        fencing: set[tuple[complex, complex]] = set()
        for plot, direction in product(region, DIRECTIONS):
            if plot + direction not in region:
                fencing.add((plot, direction))
        total_cost_part_1 += len(fencing) * area

        # Count sides by taking fence panels and extending them to the left and right,
        # removing the neighbouring panels as we go
        n_sides = 0
        while fencing:
            plot, direction = fencing.pop()
            n_sides += 1
            for left_right_direction in LEFT_RIGHT[direction]:
                neighbour = plot + left_right_direction
                while neighbour in region:
                    if (neighbour, direction) not in fencing:  # Side has ended
                        break
                    fencing.remove((neighbour, direction))
                    neighbour += left_right_direction
        total_cost_part_2 += n_sides * area

    print(f"Part 1: {total_cost_part_1}")
    print(f"Part 2: {total_cost_part_2}\n")


solve(example_input)
solve(actual_input)
