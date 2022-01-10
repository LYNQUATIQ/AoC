"""https://adventofcode.com/2018/day/9"""

from utils import print_time_taken


actual_input = 864801


@print_time_taken
def solve(target_length, target_number):
    recipes = {0: 3, 1: 7}
    elf1, elf2 = 0, 1
    total_recipes = 2
    num_digits = 10 ** (len(str(target_number)))
    most_recent = 37
    done = False
    while not done:
        total = recipes[elf1] + recipes[elf2]
        for recipe in divmod(total, 10) if total > 9 else (total,):
            recipes[total_recipes] = recipe
            total_recipes += 1
            most_recent = (most_recent * 10 + recipe) % num_digits
            if most_recent == target_number:
                done = True
                break
        elf1 = (elf1 + recipes[elf1] + 1) % total_recipes
        elf2 = (elf2 + recipes[elf2] + 1) % total_recipes

    next10 = "".join(str(recipes[i]) for i in range(target_length, target_length + 10))
    print(f"Part 1: {next10}")
    print(f"Part 2: {total_recipes - len(str(target_number))}\n")


solve(9, 92510)
solve(actual_input, actual_input)
