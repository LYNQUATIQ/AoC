import os
import re

from collections import namedtuple
from itertools import combinations_with_replacement, permutations


with open(os.path.join(os.path.dirname(__file__), "inputs/day15_input.txt")) as f:
    actual_input = f.read()

example_input = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""

regex = re.compile(
    r"^(\w+): capacity ([-]?\d+), durability ([-]?\d+), flavor ([-]?\d+), texture ([-]?\d+), calories ([-]?\d+)$"
)

Ingredient = namedtuple("Ingredient", "capacity durability flavor texture calories")


def solve(inputs):
    ingredients = {}
    for data in (regex.match(line).groups() for line in inputs.splitlines()):
        ingredients[data[0]] = Ingredient(*(int(c) for c in data[1:]))

    weight_combos = [
        r
        for r in combinations_with_replacement(range(101), len(ingredients) - 1)
        if sum(r) <= 100
    ]

    def max_score(calorie_count=None):
        max_score = 0
        for weights in weight_combos:
            recipes = permutations([w for w in weights] + [100 - sum(weights)])
            for r in recipes:
                capacity, durability, flavor, texture, calories = 0, 0, 0, 0, 0
                for ingredient, w in zip(ingredients.values(), r):
                    capacity += w * ingredient.capacity
                    durability += w * ingredient.durability
                    flavor += w * ingredient.flavor
                    texture += w * ingredient.texture
                    calories += w * ingredient.calories
                score = (
                    max(capacity, 0)
                    * max(durability, 0)
                    * max(flavor, 0)
                    * max(texture, 0)
                )
                if calorie_count is None or calories == calorie_count:
                    max_score = max(score, max_score)
        return max_score

    print(f"Part 1: {max_score()}")
    print(f"Part 2: {max_score(calorie_count=500)}\n")


solve(example_input)
solve(actual_input)
