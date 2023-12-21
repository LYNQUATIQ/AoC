"""https://adventofcode.com/2023/day/21"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day21_input.txt")) as f:
    actual_input = f.read()


sample_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

ROCK = "#"


def solve(inputs: str, steps_to_take: int):
    plots: set[tuple[int, int]] = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c != ROCK:
                plots.add((x, y))
    width, height = x + 1, y + 1
    start = (width // 2, height // 2)

    paths, to_visit = {start: 0}, {(start, 0)}
    while to_visit:
        xy, steps_to_here = to_visit.pop()
        steps_to_next = steps_to_here + 1
        for dx, dy in ((0, -1), (0, 1), (1, 0), (-1, 0)):
            next_xy = (xy[0] + dx, xy[1] + dy)
            best_so_far = paths.get(next_xy, steps_to_next + 1)
            if next_xy in plots and steps_to_next < best_so_far:
                paths[next_xy] = steps_to_next
                to_visit.add((next_xy, steps_to_next))

    odd_plots = {xy for xy in paths if paths[xy] % 2}
    even_plots = {xy for xy in paths if xy not in odd_plots}
    possible_plots = odd_plots if steps_to_take % 2 else even_plots
    print(f"\nPart 1: {sum(paths[xy] <= steps_to_take for xy in possible_plots)}")

    if steps_to_take != 64:
        return

    # Note that 26_501_365 = 131 * 202300 + 65
    extent = 202300
    assert width == 131 and height == 131
    assert 26_501_365 == extent * width + width // 2
    assert 26_501_365 == extent * height + height // 2

    odd_grids, even_grids = (extent + 1) ** 2, extent**2
    even_65 = sum(paths[xy] <= 65 for xy in even_plots)
    odd_65 = sum(paths[xy] <= 65 for xy in odd_plots)
    reachable = odd_grids * len(odd_plots) + even_grids * len(even_plots)
    reachable += extent * (len(even_plots) - even_65)
    reachable -= (extent + 1) * (len(odd_plots) - odd_65)
    print(f"Part 2: {reachable}")


solve(sample_input, 6)
solve(actual_input, 64)
