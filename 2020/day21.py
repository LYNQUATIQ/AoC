import os
import random

from collections import defaultdict
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day21_input.txt")) as f:
    actual_input = f.read()

sample_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


@print_time_taken
def solve(inputs):
    ingredient_count = defaultdict(int)
    ingredient_allergens = defaultdict(set)
    allergen_ingredients = defaultdict(set)

    foods = []
    for food, allergens in (l[:-1].split(" (contains ") for l in inputs.splitlines()):
        foods.append((food.split(), allergens.split(", ")))

    for ingredients, allergens in foods:
        for ingredient in ingredients:
            ingredient_count[ingredient] += 1
            ingredient_allergens[ingredient].update(allergens)
        for allergen in allergens:
            allergen_ingredients[allergen].update(ingredients)

    for ingredients, allergens in foods:
        for allergen in allergens:
            for ingredient in allergen_ingredients[allergen]:
                if ingredient not in ingredients:
                    ingredient_allergens[ingredient].discard(allergen)

    allergen_map = {}
    part1 = 0
    while ingredient_count:
        ingredient = random.choice(list(ingredient_count))
        allergens = ingredient_allergens[ingredient]
        if len(allergens) > 1:
            continue
        if not allergens:
            part1 += ingredient_count[ingredient]
        else:
            allergen = next(iter(allergens))
            allergen_map[allergen] = ingredient
            for i in ingredient_allergens:
                ingredient_allergens[i].discard(allergen)
        del ingredient_count[ingredient]

    print(f"Part 1: {part1}")
    print(f"Part 2: {','.join(allergen_map[a] for a in sorted(allergen_map))}\n")


solve(sample_input)
solve(actual_input)
