"""https://adventofcode.com/2023/day/17"""
import os

from collections.abc import Generator
from heapq import heappop, heappush
from typing import Iterable


with open(os.path.join(os.path.dirname(__file__), "inputs/day17_input.txt")) as f:
    actual_input = f.read()


sample_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


Xy = tuple[int, int]
State = tuple[Xy, Xy]  # State is a location and a next direction


class Grid:
    def __init__(self, inputs: str) -> None:
        self.grid = [list(map(int, (c for c in line))) for line in inputs.splitlines()]
        self.width, self.height = len(self.grid[0]), len(self.grid)

    def is_valid_location(self, xy: Xy) -> bool:
        return (0 <= xy[0] < self.width) and (0 <= xy[1] < self.height)

    def get(self, xy: Xy) -> int:
        return self.grid[xy[1]][xy[0]]


def possible_next_states(
    this_state: State, grid: Grid, min_steps: int, max_steps: int
) -> Generator[Iterable[tuple[State, int]]]:
    xy, direction = this_state
    turn_right = (direction[1], direction[0])
    turn_left = (direction[1] * -1, direction[0] * -1)
    additional_heat_loss = 0
    next_xy = xy
    for n_steps in range(max_steps):
        next_xy = (next_xy[0] + direction[0], next_xy[1] + direction[1])
        if not grid.is_valid_location(next_xy):
            break
        additional_heat_loss += grid.get(next_xy)
        if n_steps < min_steps - 1:
            continue
        yield ((next_xy, turn_right), additional_heat_loss)
        yield ((next_xy, turn_left), additional_heat_loss)


def manhattan_distance(a: Xy, b: Xy) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def best_path(grid: Grid, max_steps: int, min_steps: int = 1) -> int:
    target = (grid.width - 1, grid.height - 1)
    start, initial_directions = (0, 0), [(0, 1), (1, 0)]
    initial_states = [(start, direction) for direction in initial_directions]
    to_visit = [(0, initial_state) for initial_state in initial_states]
    heat_losses = {initial_state: 0 for initial_state in initial_states}
    while to_visit:
        _, this_state = heappop(to_visit)
        if this_state[0] == target:
            return heat_losses[this_state]
        next_states = possible_next_states(this_state, grid, min_steps, max_steps)
        for next_state, additional_heat_loss in next_states:
            heat_loss = heat_losses[this_state] + additional_heat_loss
            if heat_loss < heat_losses.get(next_state, heat_loss + 1):
                heat_losses[next_state] = heat_loss
                f_score = heat_loss + manhattan_distance(next_state[0], target)
                heappush(to_visit, (f_score, next_state))
    raise RuntimeError("Never got to target")


def solve(inputs: str):
    grid = Grid(inputs)
    print(f"Part 1: {best_path(grid, max_steps=3)}")
    print(f"Part 2: {best_path(grid, min_steps=4, max_steps=10)}\n")


solve(sample_input)
solve(actual_input)
