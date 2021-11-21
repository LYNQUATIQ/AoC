import os
import re


with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()

actual_input = actual_input.replace("Rn", "(")
actual_input = actual_input.replace("Ar", ")")
actual_input = actual_input.replace("Y", "|")

data, medicine = actual_input.split("\n\n")

replacements = dict(list(l.split(" => ")[::-1] for l in data.splitlines()))

RN_AR = re.compile(r"(?P<header>Th|Ti|P|Si|C|N|O)\((?P<content>[A-Za-z|]+)\)")
REGEX = re.compile("(?P<replacement>" + "|".join(set(replacements)) + r")(\(|$)")


def find_recipe(target):
    print(f"LOOKING FOR: {target}")
    steps = []

    while RN_AR.search(target) or REGEX.search(target):
        while match := RN_AR.search(target):
            print("RN_AR:", match)
            sub_targets = []
            for sub_target in match.group("content").split("|"):
                molecule, recipe = find_recipe(sub_target)
                sub_targets.append(molecule), steps.extend(recipe)
            replacement = match.group("header") + "(" + "|".join(sub_targets) + ")"
            steps += [replacement]
            target = RN_AR.sub(replacements[replacement], target, count=1)
            print(f"  Replacing {replacement} with {replacements[replacement]}")
            print(
                f"  New target:\n{target}\n{len(target)} characters - {target.count('(')} x ('s, {target.count(')')} x )'s\n"
            )
        while match := REGEX.search(target):
            print("REGEX:", match)
            replacement = match.group("replacement")
            steps += [replacement]
            left, right = match.span()
            target = target[:left] + replacements[replacement] + target[right:]
            print(f"  Replacing {replacement} with {replacements[replacement]}")
            print(
                f"  New target:\n{target}\n{len(target)} characters - {target.count('(')} x ('s, {target.count(')')} x )'s\n"
            )

    # print(f"FOUND: {target}")

    return target, steps


def possible_molecules(seed):
    molecules = set()
    for target, source in replacements.items():
        for m in re.finditer(source, seed):
            molecules.add(seed[: m.span()[0]] + target + seed[m.span()[1] :])
    return molecules


print(f"Part 1: {len(possible_molecules(medicine))}")

seed, recipe = find_recipe(medicine)
print(f"Part 2: SEED={seed}  {len(recipe)}\n")
