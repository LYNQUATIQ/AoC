from collections import defaultdict
from itertools import cycle


class DoubleLinkedNode:
    def __init__(self, value, prior_node=None, next_node=None):

        if prior_node is None:
            prior_node = self
        self.prior_node = prior_node
        if next_node is None:
            next_node = self
        self.next_node = next_node
        self.value = value

    def insert_after(self, value):
        new_node = DoubleLinkedNode(value, self, self.next_node)
        self.next_node.prior_node = new_node
        self.next_node = new_node
        return new_node

    def insert_before(self, value):
        new_node = DoubleLinkedNode(value, self.prior_node, self)
        self.prior_node.next_node = new_node
        self.prior_node = new_node
        return new_node


first_recipe = DoubleLinkedNode(3)
second_recipe = first_recipe.insert_after(7)
number_of_recipes = 2

ELF1 = 0
ELF2 = 1
elves = [ELF1, ELF2]
current_recipes = {
    ELF1: first_recipe,
    ELF2: second_recipe,
}


target = "864801"
latest_recipes = "37"
while latest_recipes != target:

    # Create new recipes
    recipe_sum = sum([r.value for r in current_recipes.values()])
    for value in [int(c) for c in str(recipe_sum)]:
        first_recipe.insert_before(value)
        number_of_recipes += 1
        latest_recipes += str(value)
        if number_of_recipes > len(target):
            latest_recipes = latest_recipes[1:]
            if latest_recipes == target:
                break

    # Change the elves recipes
    for elf in elves:
        for _ in range(current_recipes[elf].value + 1):
            current_recipes[elf] = current_recipes[elf].next_node

print(number_of_recipes - len(target))
