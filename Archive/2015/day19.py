import os
import re


with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()

actual_input = actual_input.replace("Rn", "<")
actual_input = actual_input.replace("Ar", ">")

data, medicine = actual_input.split("\n\n")
print(medicine)
replacements = dict(list(l.split(" => ")[::-1] for l in data.splitlines()))

REPLACEMENTS = re.compile("(?P<replacement>(" + "|".join(set(replacements)) + "))")
RN_AR = re.compile("<(?P<contents>[A-QS-Za-z]*)>")
RN_AR_SEEDS = set(
    m.group("contents") for m in (RN_AR.search(r) for r in replacements) if m
)
SEED = "e"

# print(RN_AR_CONTENTS)
# input()


def find_recipe(target):

    print(f"FINDING RECIPE FOR:\n{target}\n{'0123456789' * (len(target)//10)}\n")
    steps = []

    if target == SEED or target in RN_AR_SEEDS:
        return target, steps

    for match in RN_AR.finditer(target):
        print(f"  RESOLVING RN_AR: {match}")
        if match.group("contents") in RN_AR_SEEDS:
            continue
        rn_ar_seed, sub_recipe = find_recipe(match.group("contents"))
        assert sub_recipe is not None
        steps += sub_recipe
        left, right = match.span()
        target = target[:left] + f"<{rn_ar_seed}>" + target[right:]
        print(f"  TARGET NOW: {target}")

    for match in REPLACEMENTS.finditer(target):
        print(f"  CHECKING: {match}")
        replacement = match.group("replacement")
        left, right = match.span()
        new_target = target[:left] + replacements[replacement] + target[right:]
        seed, recipe = find_recipe(new_target)
        if recipe is not None:
            return seed, steps + [replacement] + recipe

    return target, None


def possible_molecules(seed):
    molecules = set()
    for target, source in replacements.items():
        for m in re.finditer(source, seed):
            molecules.add(seed[: m.span()[0]] + target + seed[m.span()[1] :])
    return molecules


print(f"Part 1: {len(possible_molecules(medicine))}")

recipe = find_recipe(medicine)
print(f"Part 2: {len(recipe)}\n")
