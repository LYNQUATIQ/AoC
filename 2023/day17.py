"""https://adventofcode.com/2023/day/17"""
import os
from heapq import heappop, heappush
from pickle import READONLY_BUFFER


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

# sample_input = """111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991"""

#  State is a location, last direction, steps taken in this direction
Xy = tuple[int, int]
State = tuple[Xy, int, Xy, int]

DIRECTIONS = (0, 1), (0, -1), (1, 0), (-1, 0)


class Grid:
    def __init__(self, inputs: str) -> None:
        self.grid = [list(map(int, (c for c in line))) for line in inputs.splitlines()]
        self.width, self.height = len(self.grid[0]), len(self.grid)

    def is_valid_location(self, xy: Xy) -> bool:
        return (0 <= xy[0] < self.width) and (0 <= xy[1] < self.height)

    def get(self, xy: Xy) -> int:
        return self.grid[xy[1]][xy[0]]


def possible_next_states(this_state, grid, min_steps, max_steps):
    xy, current_direction, n_steps = this_state
    go_back = (current_direction[0] * -1, current_direction[1] * -1)
    next_states = []
    pass
    for next_direction in DIRECTIONS:
        if next_direction == go_back:
            continue
        if (next_direction != current_direction) and (n_steps < min_steps):
            continue
        if (next_direction == current_direction) and (n_steps == max_steps):
            continue
        next_xy = (xy[0] + next_direction[0], xy[1] + next_direction[1])
        if grid.is_valid_location(next_xy):
            next_n_steps = n_steps + 1 if (next_direction == current_direction) else 1
            next_state = (next_xy, next_direction, next_n_steps)
            # yield next_state
            next_states.append(next_state)

    return next_states


def manhattan_distance(a: Xy, b: Xy) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def best_path(grid, min_steps: int = 0, max_steps: int = 3) -> int:
    target = (grid.width - 1, grid.height - 1)
    initial_state = ((0, 0), (0, 0), 5)
    to_visit = [(0, initial_state)]
    heat_losses = {initial_state: 0}
    prior_state = {initial_state: None}

    # Do an a* search
    while to_visit:
        _, this_state = heappop(to_visit)
        if this_state[0] == target and this_state[2] >= min_steps:
            # s = this_state
            # path = [s]
            # while s is not None:
            #     path.append(s)
            #     s = prior_state[s]
            # for s in path[::-1]:
            #     print(s[0], s[2])
            return heat_losses[this_state]

        for next_state in possible_next_states(this_state, grid, min_steps, max_steps):
            new_location = next_state[0]
            heat_loss = heat_losses[this_state] + grid.get(new_location)
            best_heat_loss_so_far = heat_losses.get(next_state, heat_loss + 1)
            if heat_loss < best_heat_loss_so_far and next_state not in [
                i[1] for i in to_visit
            ]:
                heat_losses[next_state] = heat_loss
                # prior_state[next_state] = this_state
                f_score = heat_loss + manhattan_distance(new_location, target)
                heappush(to_visit, (f_score, next_state))

    raise RuntimeError("Never got to target")


def solve(inputs: str):
    grid = Grid(inputs)

    print(f"Part 1: {best_path(grid, max_steps=3)}")
    print(f"Part 2: {best_path(grid, min_steps=4, max_steps=10)}\n")


solve(sample_input)
solve(actual_input)
