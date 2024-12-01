"""https://adventofcode.com/2018/day/9"""

from utils import print_time_taken


INITIAL_RECIPES = 37


@print_time_taken
def solve(part1_length, target):
    elf1, elf2, recipes = 0, 1, list(divmod(INITIAL_RECIPES, 10))
    most_recent, target_modulo = INITIAL_RECIPES, 10 ** (len(str(target)))
    done = False
    while not done:
        elf1_quality, elf2_quality = recipes[elf1], recipes[elf2]
        total = elf1_quality + elf2_quality
        for recipe in divmod(total, 10) if total > 9 else (total,):
            recipes.append(recipe)
            most_recent = (most_recent * 10 + recipe) % target_modulo
            if most_recent == target:
                done = True
                break
        elf1 = (elf1 + elf1_quality + 1) % len(recipes)
        elf2 = (elf2 + elf2_quality + 1) % len(recipes)

    next10 = "".join(str(recipes[i]) for i in range(part1_length, part1_length + 10))
    print(f"Part 1: {next10}")
    print(f"Part 2: {len(recipes) - len(str(target))}\n")


solve(9, 92510)
solve(864801, 864801)
