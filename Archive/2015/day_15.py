import logging
import os

import re

from itertools import combinations_with_replacement, permutations
from typing import NamedTuple

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

regex = re.compile(r"^(?P<ingredient>\w+): capacity (?P<capacity>[-]*\d+), durability (?P<durability>[-]*\d+), flavor (?P<flavor>[-]*\d+), texture (?P<texture>[-]*\d+), calories (?P<calories>[-]*\d+)$")

class Ingredient(NamedTuple("Ingredient", [("capacity", int), ("durability", int), ("flavor", int), ("texture", int), ("calories", int)])):
    pass

ingredients = {}
for line in lines:
    params = regex.match(line).groupdict()
    components = {c: int(params[c]) for c in ["capacity", "durability", "flavor", "texture", "calories"]}
    ingredients[params["ingredient"]] = Ingredient(**components)

weight_combos = [r for r in combinations_with_replacement(range(101), len(ingredients) - 1) if sum(r) <= 100]

def max_score(calorie_count=None):
    max_score = 0
    for weights in weight_combos:
        recipes = permutations([w for w in weights] + [100-sum(weights)])
        for r in recipes:
            capacity = 0
            durability = 0
            flavor = 0
            texture = 0        
            calories = 0        
            for ingredient, w in zip(ingredients.values(), r):
                capacity += w * ingredient.capacity
                durability += w * ingredient.durability
                flavor += w * ingredient.flavor
                texture += w * ingredient.texture
                calories += w * ingredient.calories
            score = max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(texture, 0)
            if calorie_count is None or calories == calorie_count:
                max_score = max(score, max_score)
    return max_score

print(f"Part 1: {max_score()}")
print(f"Part 2: {max_score(calorie_count=500)}")