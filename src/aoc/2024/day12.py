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

NORTH, EAST, SOUTH, WEST = -1j, 1, 1j, -1
SIDES = (NORTH, EAST, SOUTH, WEST)
LEFT_RIGHT = {
    NORTH: (WEST, EAST),
    EAST: (NORTH, SOUTH),
    SOUTH: (EAST, WEST),
    WEST: (SOUTH, NORTH),
}


def solve(inputs: str):
    grid = {}
    for y, row in enumerate(inputs.splitlines()):
        for x, plant in enumerate(row):
            grid[complex(x, y)] = plant

    regions, regions_to_check = [], set(grid.keys())
    while regions_to_check:
        xy = regions_to_check.pop()
        region, regional_plant = {xy}, grid[xy]
        to_visit = {xy}
        while to_visit:
            xy = to_visit.pop()
            for neighbour_xy in [xy + d for d in SIDES]:
                if neighbour_xy in region or grid.get(neighbour_xy) != regional_plant:
                    continue
                region.add(neighbour_xy)
                to_visit.add(neighbour_xy)
                regions_to_check.discard(neighbour_xy)
        regions.append(region)

    total_cost_part_1 = 0
    total_cost_part_2 = 0
    for region in regions:
        area, fencing, n_sides = len(region), set(), 0

        # Find all the fence panels in the region (noting position and side)
        for xy in region:
            for side in SIDES:
                if xy + side not in region:
                    fencing.add((xy, side))
        total_cost_part_1 += len(fencing) * area

        # Count sides by removing panels that are part of that side (going left/right)
        while fencing:
            n_sides += 1
            xy, side = fencing.pop()
            left, right = LEFT_RIGHT[side]
            left_xy, right_xy = xy + left, xy + right
            while left_xy in region:
                if (left_xy, side) not in fencing:
                    break
                fencing.remove((left_xy, side))
                left_xy += left
            while right_xy in region:
                if (right_xy, side) not in fencing:
                    break
                fencing.remove((right_xy, side))
                right_xy += right
        total_cost_part_2 += n_sides * area

    print(f"Part 1: {total_cost_part_1}")
    print(f"Part 2: {total_cost_part_2}\n")


solve(example_input)
solve(actual_input)
