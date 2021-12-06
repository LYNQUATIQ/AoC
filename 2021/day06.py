import os

from collections import Counter, defaultdict

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day06_input.txt")) as f:
    actual_input = f.read()

sample_input = """3,4,3,1,2"""


@print_time_taken
def solve(inputs):
    def count_fish(n):
        fish = defaultdict(int, Counter(map(int, inputs.split(","))))
        for _ in range(n):
            spawning_fish = fish[0]
            fish = {k: fish[k + 1] for k in range(8)}
            fish[8] = spawning_fish
            fish[6] += spawning_fish

        return sum(fish.values())

    print(f"Part 1: {count_fish(80)}")
    print(f"Part 2: {count_fish(256)}\n")


solve(sample_input)
solve(actual_input)
