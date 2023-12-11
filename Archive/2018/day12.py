"""https://adventofcode.com/2018/day/12"""
import os

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day12_input.txt")) as f:
    actual_input = f.read()

sample_input = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""


PLANT, EMPTY = "#", "."


@print_time_taken
def solve(inputs):
    initial, rules = inputs.split("\n\n")

    rules = dict(tuple(line.split(" => ")) for line in rules.splitlines())
    initial_state = initial.split()[2]

    iteration, base_index, state = 0, 0, initial_state
    while iteration < 50_000_000_000:
        iteration += 1
        prior_state = state
        state = "..." + state + "..."
        base_index -= 1
        next_state = ""
        for i in range(2, len(state) - 2):
            next_state += rules.get(state[i - 2 : i + 3], EMPTY)
        state = next_state
        next_state = next_state.lstrip(".")
        base_index += len(state) - len(next_state)
        state = next_state.rstrip(".")

        if iteration == 20:
            print(
                "Part 1: ",
                sum(i for i, c in enumerate(state, base_index) if c == PLANT),
            )
        if state == prior_state:
            break

    base_index += 50_000_000_000 - iteration
    print(f"Part 2: {sum(i for i, c in enumerate(state, base_index) if c == PLANT)}\n")


solve(sample_input)
solve(actual_input)
