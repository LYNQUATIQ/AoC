import logging
import os

from typing import NamedTuple


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)


class Item(NamedTuple("Item", [("item_type", str), ("name", str)])):
    GENERATOR = "generator"
    MICROCHIP = "microchip"

    def __repr__(self):
        return f"{self.name} {self.item_type}"

    @property
    def partner(self):
        if self.item_type == self.GENERATOR:
            return Item(self.MICROCHIP, self.name)
        return Item(self.GENERATOR, self.name)


class Floor:
    def __init__(self, items=set()):
        self.items = items

    @property
    def is_empty(self):
        return not self.items

    @property
    def generators(self):
        return [g for g in self.items if g.item_type == Item.GENERATOR]

    @property
    def microchips(self):
        return [m for m in self.items if m.item_type == Item.MICROCHIP]

    @property
    def singleton_microchips(self):
        return [m for m in self.microchips if m.partner not in self.items]

    @property
    def first_pair(self):
        if self.generators:
            return [
                (g, g.partner) for g in self.generators if g.partner in self.microchips
            ][0]
        return tuple(self.microchips[0:2])


class RadiationContainment:

    def __init__(self, floors):
        self.floors = {}
        self.item_levels = {}
        self.current_level = 1

        for level, items in floors.items():
            generators = set([Item(Item.GENERATOR, g) for g in items[0]])
            microchips = set([Item(Item.MICROCHIP, g) for g in items[1]])
            floor = Floor(generators | microchips)
            self.floors[level] = floor
            for item in floor.items:
                self.item_levels[item] = level

    def print_floors(self):
        def item_list(items, uppercase):
            list_str = "|".join([i.name[0:3] for i in items])
            if uppercase:
                list_str = list_str.upper()
            else:
                list_str = list_str.lower()
            return list_str

        for l in range(4, 0, -1):
            f = self.floors[l]
            elevator = "   "
            if self.current_level == l:
                elevator = "[E]"
            print(
                f"Floor#{l} {elevator} {item_list(f.generators, True)} {item_list(f.microchips, False)}"
            )
        print()

    def move_items_up(self, items):
        self.move_items(items, +1)

    def move_items_down(self, items):
        self.move_items(items, -1)

    def move_items(self, items, move):
        new_level = self.current_level + move
        for item in items:
            self.floors[self.current_level].items.remove(item)
            self.floors[new_level].items.add(item)
            self.item_levels[item] = new_level
        self.current_level = new_level

    def best_microchip_to_move_down(self):
        floor = self.floors[self.current_level]
        if floor.singleton_microchips:
            return floor.singleton_microchips[0]
        return floor.microchips[0]

    def steps(self):
        steps = 0
        # Assume I'm on the lowest non-empty floor
        while True:
            pair = self.floors[self.current_level].first_pair
            self.move_items_up(pair)
            steps += 1
            if self.floors[self.current_level - 1].is_empty:
                if self.current_level == 4:
                    break
                continue
            self.move_items_down([self.best_microchip_to_move_down()])
            steps += 1

        return steps


floors = {
    4: ([], []),
    3: ([], []),
    2: ([], ["polonium", "promethium"]),
    1: (
        ["polonium", "thulium", "promethium", "ruthenium", "cobalt"],
        ["thulium", "ruthenium", "cobalt"],
    ),
}
print(f"Part 1: {RadiationContainment(floors).steps()}")

floors = {
    4: ([], []),
    3: ([], []),
    2: ([], ["polonium", "promethium"]),
    1: (
        [
            "polonium",
            "thulium",
            "promethium",
            "ruthenium",
            "cobalt",
            "elerium",
            "dilithium",
        ],
        ["thulium", "ruthenium", "cobalt", "elerium", "dilithium"],
    ),
}
print(f"Part 2: {RadiationContainment(floors).steps()}")
