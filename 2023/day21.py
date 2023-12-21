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

EXTENT = 202300


def solve(inputs: str, steps_to_take: int):
    plots: set[tuple[int, int]] = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c != ROCK:
                plots.add((x, y))
    width, height = x + 1, y + 1
    start = (width // 2, height // 2)

    shortest_paths = {start: 0}
    to_visit = {(start, 0)}
    while to_visit:
        xy, steps_to_here = to_visit.pop()
        steps_to_next = steps_to_here + 1
        for dx, dy in ((0, -1), (0, 1), (1, 0), (-1, 0)):
            next_xy = (xy[0] + dx, xy[1] + dy)
            best_so_far = shortest_paths.get(next_xy, steps_to_next + 1)
            if next_xy in plots and steps_to_next < best_so_far:
                shortest_paths[next_xy] = steps_to_next
                to_visit.add((next_xy, steps_to_next))

    odds = {xy for xy in shortest_paths if shortest_paths[xy] % 2}
    evens = {xy for xy in shortest_paths if xy not in odds}
    candidates = odds if steps_to_take % 2 else evens

    print(f"\nPart 1: {sum(shortest_paths[xy] <= steps_to_take for xy in candidates)}")

    if steps_to_take != 64:
        return

    # Note that 26501365 = 131 * 202300 + 65
    assert width == 131 and height == 131
    assert 26_501_365 == EXTENT * width + width // 2
    assert 26_501_365 == EXTENT * height + height // 2

    odd_grids, even_grids = (EXTENT + 1) ** 2, EXTENT**2
    even_113, odd_113 = len(evens), len(odds)
    even_65 = sum(shortest_paths[xy] <= 65 for xy in evens)
    odd_65 = sum(shortest_paths[xy] <= 65 for xy in odds)
    reachable = odd_grids * odd_113 + even_grids * even_113
    reachable += EXTENT * (even_113 - even_65)
    reachable -= (EXTENT + 1) * (odd_113 - odd_65)
    print(f"Part 2: {reachable}")


solve(sample_input, 6)
solve(actual_input, 64)
