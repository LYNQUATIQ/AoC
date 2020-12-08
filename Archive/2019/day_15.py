import os

from grid_system import XY, ConnectedGrid
from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]


class OxygenSystem(ConnectedGrid):

    OPEN = " "
    WALL = "#"
    O2_SYSTEM = "*"
    OXYGEN = "O"
    TO_CHECK = "?"

    SYMBOLS = {0: WALL, 1: OPEN, 2: O2_SYSTEM}

    MOVE_NORTH = 1
    MOVE_SOUTH = 2
    MOVE_WEST = 3
    MOVE_EAST = 4

    DIRECTIONS = {
        ConnectedGrid.NORTH: MOVE_NORTH,
        ConnectedGrid.SOUTH: MOVE_SOUTH,
        ConnectedGrid.EAST: MOVE_EAST,
        ConnectedGrid.WEST: MOVE_WEST,
    }

    def __init__(self, program):
        super().__init__()
        self.computer = IntCodeComputer(program)
        self.origin = XY(0, 0)
        self.robot = self.origin
        self.grid[self.robot] = self.OPEN
        self.o2_system = None
        self.map_system()

    def get_symbol(self, xy, char_map={}):
        symbol = self.grid.get(xy, " ")
        c = char_map.get(symbol, symbol)
        if xy == self.robot:
            c = "\u2588"
        return c

    def move_robot(self, neighbour):
        direction = neighbour - self.robot
        retval = self.computer.run_program([self.DIRECTIONS[direction]])
        self.grid[neighbour] = self.SYMBOLS[retval]
        if self.grid[neighbour] == self.WALL:
            return False
        self.robot = neighbour
        if self.grid[self.robot] == self.O2_SYSTEM:
            self.o2_system = self.robot
        return True

    def connected_nodes(self, node):
        return [n for n in node.neighbours if self.grid.get(n, self.WALL) != self.WALL]

    def nodes_to_check(self):
        return set(k for k, v in self.grid.items() if v == self.TO_CHECK)

    def map_system(self):
        self.grid.update({n: self.TO_CHECK for n in self.robot.neighbours})
        visited = set(self.robot)
        while self.nodes_to_check():
            paths_to_visit = self.paths_to_goals(self.robot, self.nodes_to_check())
            shortest_path = sorted(paths_to_visit.values(), key=len)[0]
            node_to_visit = shortest_path[-1]
            next_step = shortest_path[0]
            while next_step != node_to_visit:
                assert self.move_robot(next_step)
                shortest_path = shortest_path[1:]
                next_step = shortest_path[0]
            if self.move_robot(node_to_visit):
                nodes_to_check = (n for n in self.robot.neighbours if n not in visited)
                self.grid.update({n: self.TO_CHECK for n in nodes_to_check})
            visited.add(self.robot)
            os.system("cls" if os.name == "nt" else "clear")
            self.print_grid()

    def flood_system(self):
        t = 0
        self.grid[self.o2_system] = self.OXYGEN

        nodes_to_flood = set(k for k, v in self.grid.items() if v == self.OPEN)
        next_to_flood = set(n for n in self.o2_system.neighbours if n in nodes_to_flood)
        while nodes_to_flood:
            t += 1
            nodes_to_flood -= next_to_flood
            new_nodes = set()
            for node in next_to_flood:
                self.grid[node] = self.OXYGEN
                new_nodes.update(set(n for n in node.neighbours if n in nodes_to_flood))
            next_to_flood = new_nodes
            os.system("cls" if os.name == "nt" else "clear")
            self.print_grid()
        return t


system = OxygenSystem(program)
print(f"Part 1: {len(system.find_shortest_path(system.origin, system.o2_system))}")
print(f"Part 2: {system.flood_system()}")