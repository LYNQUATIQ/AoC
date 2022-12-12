"""https://adventofcode.com/2022/day/12"""
import os

from heapq import heappop, heappush
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


@print_time_taken
def solve(inputs: str) -> None:
    start, target = (0, 0), (0, 0)
    grid: dict[tuple[int, int], int] = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            xy, elevation = (x, y), ord(c) - ord("a")
            if c == "S":
                start, elevation = xy, 0
            elif c == "E":
                target, elevation = xy, 25
            grid[xy] = elevation

    possible_steps = {}
    for xy in grid:
        steps = []
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            step = (xy[0] + dx, xy[1] + dy)
            if grid.get(step, 99) - grid[xy] <= 1:
                steps.append(step)
        possible_steps[xy] = tuple(steps)

    def find_shortest_path(start: tuple[int, int], best_so_far: int = len(grid)) -> int:
        visited: set[tuple[int, int]] = set()
        distance_to = {start: 0}
        to_visit: list[tuple[float, tuple[int, int]]] = []
        heappush(to_visit, (0, start))
        while to_visit:
            _, this_node = heappop(to_visit)
            if this_node == target:
                return distance_to[this_node]
            visited.add(this_node)
            if distance_to[this_node] >= best_so_far:
                continue
            for next_node in possible_steps[this_node]:
                distance_to_here = distance_to[this_node] + 1
                prior_distance_to_here = distance_to.get(next_node, 0)
                if next_node in visited and distance_to_here >= prior_distance_to_here:
                    continue
                if distance_to_here < prior_distance_to_here or next_node not in [
                    i[1] for i in to_visit
                ]:
                    distance_to[next_node] = distance_to_here
                    h_score = (
                        abs(next_node[0] - target[0])
                        + abs(next_node[1] - target[1])
                        - grid[next_node]
                    )
                    f_score = distance_to_here + h_score
                    heappush(to_visit, (f_score, next_node))
        return 999999

    best_so_far = find_shortest_path(start)
    print(f"Part 1: {best_so_far}")

    for possible_start in [n for n, e in grid.items() if e == 0 and n != start]:
        path_length = find_shortest_path(possible_start, best_so_far)
        best_so_far = min(path_length, best_so_far)
    print(f"Part 2: {best_so_far}\n")


solve(sample_input)
solve(actual_input)
