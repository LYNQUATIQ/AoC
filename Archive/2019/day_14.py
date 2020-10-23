import math
import re


from collections import defaultdict

lines = [line.rstrip("\n") for line in open("2019_day14_input.txt")]

pattern = re.compile("^(?P<inputs>[0-9A-Z, ]+) => (?P<output>\d+ [A-Z]+)$")


class Recipe:
    def __init__(self, inputs, output):
        def read_recipe_component(input_str):
            q, c = input_str.split(" ")
            return (int(q), c)

        self.quantity, self.chemical = read_recipe_component(output)
        self.inputs = []
        for i in inputs:
            self.inputs.append(read_recipe_component(i))

    def __repr__(self):
        return f" {'+'.join([str(q)+c for q,c in self.inputs])}==>{self.quantity}{self.chemical}"


recipe_list = {}

for line in lines:

    params = pattern.match(line).groupdict()
    inputs = params["inputs"].split(", ")
    output = params["output"]
    recipe = Recipe(inputs, output)
    recipe_list[recipe.chemical] = recipe


class FuelManufacturer:
    def __init__(self, recipe_list, fuel_requirement=1):
        self.recipe_list = recipe_list
        self.chemical_store = defaultdict(int)
        self.input_requirements = defaultdict(int)

    def get_chemical(self, quantity, chemical):
        if chemical == "ORE" and self.chemical_store["ORE"] < quantity:
            return False

        self.chemical_store[chemical] -= quantity
        if self.chemical_store[chemical] < 0:
            required = -1 * self.chemical_store[chemical]
            recipe = self.recipe_list[chemical]
            n = math.ceil(required / recipe.quantity)
            for q, c in recipe.inputs:
                self.input_requirements[c] += n * q
            self.chemical_store[chemical] += n * recipe.quantity
        return True

    def process_fuel(self, fuel=1):
        self.input_requirements["FUEL"] += fuel
        while len(self.input_requirements) > 0:
            chemical = next(iter(self.input_requirements))
            quantity = self.input_requirements[chemical]
            del self.input_requirements[chemical]
            if not self.get_chemical(quantity, chemical):
                return False
        return True

    def maximise_fuel(self, ore=1000000000000):
        self.chemical_store["ORE"] = ore
        self.fuel_manafactured = 0
        while self.process_fuel():
            self.fuel_manafactured += 1

        return self.fuel_manafactured


fm = FuelManufacturer(recipe_list)
print(fm.maximise_fuel())
