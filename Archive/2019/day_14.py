import math
import os

from collections import defaultdict
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Recipe:
    FUEL = "FUEL"
    ORE = "ORE"

    def __init__(self, raw_inputs, raw_output):
        def read_raw_component(component):
            q, c = component.split(" ")
            return (int(q), c)

        self.quantity, self.chemical = read_raw_component(raw_output)
        self.inputs = [read_raw_component(i) for i in raw_inputs.split(", ")]

    def __repr__(self):
        return f" {' + '.join([str(q)+'x'+c for q,c in self.inputs])} ==> {self.quantity}{self.chemical}"


recipe_list = {}
for line in lines:
    recipe = Recipe(*line.split(" => "))
    recipe_list[recipe.chemical] = recipe


def ore_requirements(fuel_to_manufacture=1):
    requirements = defaultdict(int, {Recipe.FUEL: fuel_to_manufacture})
    ore_requirements = 0
    chemical_store = defaultdict(int)
    while requirements:
        chemical = next(iter(requirements))
        quantity_required = requirements[chemical]
        del requirements[chemical]

        available_from_store = min(chemical_store[chemical], quantity_required)
        chemical_store[chemical] -= available_from_store
        quantity_required -= available_from_store

        if quantity_required == 0:
            continue

        if chemical == Recipe.ORE:
            ore_requirements += quantity_required
            continue

        recipe = recipe_list[chemical]
        recipes_made = math.ceil(quantity_required / recipe.quantity)
        for q, c in recipe_list[chemical].inputs:
            requirements[c] += q * recipes_made
        surplus = recipes_made * recipe.quantity - quantity_required
        chemical_store[chemical] += surplus

    return ore_requirements


part1 = ore_requirements(1)
print(f"Part 1: {part1}")

AVAILABLE = 1000000000000
min_search, max_search = AVAILABLE // part1, AVAILABLE
while min_search != max_search - 1:
    mid_search = (max_search - min_search) // 2 + min_search
    if ore_requirements(mid_search) > AVAILABLE:
        max_search = mid_search
    else:
        min_search = mid_search
print(f"Part 2: {min_search}")
