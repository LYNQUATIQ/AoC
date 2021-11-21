import os
import re


with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()

actual_input = actual_input.replace("Rn", "<")
actual_input = actual_input.replace("Ar", ">")
actual_input = actual_input.replace("Y", ",")

data, medicine = actual_input.split("\n\n")
print(medicine)
replacements = dict(list(l.split(" => ")[::-1] for l in data.splitlines()))

rn_ar_reps = {k: v for k, v in replacements.items() if "<" in k}
rn_ar_headers = {x.split("<")[0] for x in rn_ar_reps}

pre_rn_ar_reps = {
    k: v for k, v in replacements.items() if "<" not in k and v in rn_ar_headers
}
other_reps = {
    k: v for k, v in replacements.items() if "<" not in k and v not in rn_ar_headers
}


REPS1 = re.compile("(?P<replacement>((" + "|".join(set(pre_rn_ar_reps)) + ")))")
REPS2 = re.compile("(?P<replacement>((" + "|".join(set(other_reps)) + ")))")
RN_AR = re.compile("(?P<replacement>((" + "|".join(set(rn_ar_reps)) + ")))")

input()


def find_recipe(target):

    steps = []

    while REPS1.search(target) or REPS2.search(target) or RN_AR.search(target):
        while match := REPS1.search(target):
            print(f"LOOKING IN: {target}\n  REPS1 match: {match}")
            replacement = match.group("replacement")
            steps += [replacement]
            left, right = match.span()
            target = target[:left] + replacements[replacement] + target[right:]
            print(f"  Replacing {replacement} with {replacements[replacement]}")
            print(
                f"  New target:\n{target}\n{len(target)} characters - {target.count('(')} x ('s, {target.count(')')} x )'s\n"
            )
        if match := REPS2.search(target):
            print(f"LOOKING IN: {target}\n  REPS2 match: {match}")
            replacement = match.group("replacement")
            steps += [replacement]
            left, right = match.span()
            target = target[:left] + replacements[replacement] + target[right:]
            print(f"  Replacing {replacement} with {replacements[replacement]}")
            print(
                f"  New target:\n{target}\n{len(target)} characters - {target.count('(')} x ('s, {target.count(')')} x )'s\n"
            )
        if match := RN_AR.search(target):
            print(f"LOOKING IN: {target}\n  RN_AR match: {match}")
            replacement = match.group("replacement")
            steps += [replacement]
            left, right = match.span()
            target = target[:left] + replacements[replacement] + target[right:]
            print(f"  Replacing {replacement} with {replacements[replacement]}")
            print(
                f"  New target:\n{target}\n{len(target)} characters - {target.count('(')} x ('s, {target.count(')')} x )'s\n"
            )

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
