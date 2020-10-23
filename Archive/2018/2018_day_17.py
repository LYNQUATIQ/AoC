import logging
import os
import re

from grid_system import ConnectedGrid, XY

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_17.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, f"inputs/2018_day_17_input.txt")
lines = [line.rstrip("\n") for line in open(file_path)]

pattern = re.compile(
    r"^(?P<xy1>x|y)=(?P<level>-?\d+), (?P<xy2>x|y)=(?P<low>-?\d+)..(?P<high>-?\d+)$"
)

clay_scans = []
for line in lines:
    regex = pattern.match(line).groupdict()
    clay_scans.append(
        {
            regex["xy1"]: range(int(regex["level"]), int(regex["level"]) + 1),
            regex["xy2"]: range(int(regex["low"]), int(regex["high"]) + 1),
        }
    )


class Reservoir(ConnectedGrid):
    CLAY = "#"
    SAND = "."
    SPRING = "+"
    FLOWING_WATER = "|"
    STANDING_WATER = "~"

    water = [STANDING_WATER, FLOWING_WATER]
    permeable_material = [SAND, FLOWING_WATER]
    impermeable_material = [CLAY, STANDING_WATER]

    def get_symbol(self, xy):
        blank = self.SAND
        if xy.y < 0:
            blank = " "
        return self.grid.get(xy, blank)

    def __init__(self, clay_scans):
        super().__init__()
        self.margin = 1
        self.spring_xy = XY(500, 0)
        self.grid[self.spring_xy] = self.SPRING
        for clay_xy in clay_scans:
            for y in clay_xy["y"]:
                for x in clay_xy["x"]:
                    self.grid[XY(x, y)] = self.CLAY

    def material(self, xy):
        return self.grid.get(xy, self.SAND)

    def flood_fill(self):
        _, _, _, max_y = self.get_limits()
        to_flood_from = [self.spring_xy]
        flooded_from = set()
        while to_flood_from:
            xy = to_flood_from.pop()
            flooded_from.add(xy)

            logging.debug(f"Flooding from{xy}... ")
            # Flow down until we hit clay (or standing water) or go pass bottom
            while self.material(xy + self.DOWN) == self.SAND and xy.y < max_y - 1:
                xy += self.DOWN
                self.grid[xy] = self.FLOWING_WATER

            logging.debug(f"   hit {xy}")
            if xy.y == max_y - 1:
                logging.debug(f"   Beyond bottom...")
                continue

            # Get left and right limits
            xy_left, xy_right = xy, xy
            while (
                self.material(xy_left + self.DOWN) in self.impermeable_material
                and self.material(xy_left + self.LEFT) != self.CLAY
            ):
                xy_left += self.LEFT
                self.grid[xy_left] = self.FLOWING_WATER
            while (
                self.material(xy_right + self.DOWN) in self.impermeable_material
                and self.material(xy_right + self.RIGHT) != self.CLAY
            ):
                xy_right += self.RIGHT
                self.grid[xy_right] = self.FLOWING_WATER

            logging.debug(f"Checking limits: {xy_left} and {xy_right}")
            # If not contained by clay then flood from left and right limits,
            # Otherwise convert to standing water and flood from one above
            if (
                self.material(xy_left + self.DOWN) in self.permeable_material
                or self.material(xy_right + self.DOWN) in self.permeable_material
            ):
                if xy_left not in flooded_from:
                    to_flood_from.append(xy_left)
                if xy_right not in flooded_from:
                    to_flood_from.append(xy_right)
            else:
                logging.debug(f"Filling with water: {xy_left} to {xy_right+self.RIGHT}")
                for x in range(xy_left.x, xy_right.x + 1):
                    self.grid[XY(x, xy.y)] = self.STANDING_WATER
                self.grid[xy + self.UP] = self.FLOWING_WATER
                to_flood_from.append(xy + self.UP)


reservoir = Reservoir(clay_scans)
reservoir.flood_fill()
reservoir.print_grid(2)

print(sum(v in reservoir.water for v in reservoir.grid.values()))
print(sum(v == reservoir.STANDING_WATER for v in reservoir.grid.values()))
