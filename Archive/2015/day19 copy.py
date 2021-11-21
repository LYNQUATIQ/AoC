import os
import re


with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()


data, medicine = actual_input.split("\n\n")
replacements = dict(list(l.split(" => ")[::-1] for l in data.splitlines()))

RECIPE = re.compile(
    r"(?P<header>\w*?)(?P<replacement>" + "|".join(set(replacements)) + r")$"
)

RN_AR_RECIPE = re.compile(r"^(?P<header>\w*?)Rn(?P<content>\w+?)Ar$")


def find_recipe(target):
    print(target)
    if target in replacements.values():
        return target, []

    match = RECIPE.match(target)
    if match:
        replacement = match.group("replacement")
        target, recipe = find_recipe(match.group("header") + replacements[replacement])
        return target, recipe + [replacement]

    match = RN_AR_RECIPE.match(target)
    new_target = match.group("header") + "Rn"
    sub_targets, sub_recipes = [], []
    for sub_target in match.group("content").split("Y"):
        t, r = find_recipe(sub_target)
        sub_targets.append(t), sub_recipes.extend(r)

    new_target = match.group("header") + "Rn" + "Y".join(sub_targets) + "Ar"
    return find_recipe(new_target) + sub_recipes


def possible_molecules(seed):
    molecules = set()
    for target, source in replacements.items():
        for m in re.finditer(source, seed):
            molecules.add(seed[: m.span()[0]] + target + seed[m.span()[1] :])
    return molecules


print(f"Part 1: {len(possible_molecules(medicine))}")

seed, recipe = find_recipe(medicine)
print(f"Part 2: SEED={seed}  {len(recipe)}\n")
