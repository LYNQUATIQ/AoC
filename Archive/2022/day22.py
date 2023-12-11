"""https://adventofcode.com/2022/day/22"""
import os

from itertools import product

with open(os.path.join(os.path.dirname(__file__), "inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


EAST, SOUTH, WEST, NORTH = 0, 1, 2, 3
HEADINGS = {EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0), NORTH: (0, -1)}
TURN_ANTICLOCKWISE = {EAST: NORTH, NORTH: WEST, WEST: SOUTH, SOUTH: EAST}
TURN_CLOCKWISE = {EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST}
TURN = {"L": TURN_ANTICLOCKWISE, "R": TURN_CLOCKWISE}


EdgeLinks = list[tuple[int, int]]
Links = list[EdgeLinks]
Faces = list[list[str]]
Layout = list[tuple[int, int]]


class ForceFieldBoard:
    def __init__(self, map_data: str) -> None:
        self.face_size = int(((map_data.count(".") + map_data.count("#")) / 6) ** 0.5)

        map_rows = [row for row in map_data.splitlines()]
        self.layout = []
        for y, x in product(range(5), range(5)):
            try:
                c = map_rows[y * self.face_size][x * self.face_size]
            except IndexError:
                c = " "
            if c != " ":
                self.layout.append((x, y))

        self.faces = []
        for offset_x, offset_y in self.layout:
            x, y = offset_x * self.face_size, offset_y * self.face_size
            self.faces.append(
                [
                    map_rows[y][x : x + self.face_size]
                    for y in range(y, y + self.face_size)
                ]
            )

    def flat_links(self) -> Links:
        links: Links = []
        for x0, y0 in self.layout:
            edge_links: EdgeLinks = []
            for heading, (dx, dy) in HEADINGS.items():
                x, y = x0 + dx, y0 + dy
                if (x, y) not in self.layout:
                    dx, dy = dx * -1, dy * -1
                    while (x + dx, y + dy) in self.layout:
                        x, y = x + dx, y + dy
                edge_links.append((self.layout.index((x, y)), heading))
            links.append(edge_links)
        return links

    def cube_links(self) -> Links:
        # TODO: Calculate programatically and remove hardwired links
        if self.face_size == 4:
            return [
                [(5, WEST), (3, SOUTH), (2, SOUTH), (1, SOUTH)],
                [(2, EAST), (4, NORTH), (5, NORTH), (0, SOUTH)],
                [(3, EAST), (4, EAST), (1, WEST), (0, EAST)],
                [(5, SOUTH), (4, SOUTH), (2, WEST), (0, NORTH)],
                [(5, EAST), (1, NORTH), (2, NORTH), (3, NORTH)],
                [(0, WEST), (1, EAST), (4, WEST), (3, WEST)],
            ]
        return [
            [(1, EAST), (2, SOUTH), (3, EAST), (5, EAST)],
            [(4, WEST), (2, WEST), (0, WEST), (5, NORTH)],
            [(1, NORTH), (4, SOUTH), (3, SOUTH), (0, NORTH)],
            [(4, EAST), (5, SOUTH), (0, EAST), (2, EAST)],
            [(1, WEST), (5, WEST), (3, WEST), (2, NORTH)],
            [(4, NORTH), (1, SOUTH), (0, SOUTH), (3, NORTH)],
        ]

    def navigate_path(self, instructions: str, as_cube=False) -> int:
        links = self.cube_links() if as_cube else self.flat_links()

        face, x, y, heading = 0, 0, 0, EAST
        i, finished = 0, False
        while not finished:
            # Check if we're turning
            if instructions[i] in "LR":
                heading = TURN[instructions[i]][heading]
                i += 1
                continue

            # If not determine the number of steps to take (noting if we're finished)
            steps = 0
            while not finished and instructions[i].isdigit():
                steps = steps * 10 + int(instructions[i])
                i += 1
                if i == len(instructions):
                    finished = True

            # Keep taking steps (navigating over edges) until we're done or hit a wall
            while steps:
                next_face, next_heading = face, heading
                if heading == EAST:
                    next_x, next_y = x + 1, y
                    if next_x >= self.face_size:
                        next_face, next_heading = links[face][heading]
                        next_x, next_y = {
                            EAST: (0, next_y),
                            SOUTH: (self.face_size - next_y - 1, 0),
                            WEST: (self.face_size - 1, self.face_size - next_y - 1),
                            NORTH: (next_y, self.face_size - 1),
                        }[next_heading]
                elif heading == SOUTH:
                    next_x, next_y = x, y + 1
                    if next_y >= self.face_size:
                        next_face, next_heading = links[face][heading]
                        next_x, next_y = {
                            EAST: (0, self.face_size - next_x - 1),
                            SOUTH: (next_x, 0),
                            WEST: (self.face_size - 1, next_x),
                            NORTH: (self.face_size - next_x - 1, self.face_size - 1),
                        }[next_heading]
                elif heading == WEST:
                    next_x, next_y = x - 1, y
                    if next_x < 0:
                        next_face, next_heading = links[face][heading]
                        next_x, next_y = {
                            EAST: (0, self.face_size - next_y - 1),
                            SOUTH: (next_y, 0),
                            WEST: (self.face_size - 1, next_y),
                            NORTH: (self.face_size - next_y - 1, self.face_size - 1),
                        }[next_heading]
                elif heading == NORTH:
                    next_x, next_y = x, y - 1
                    if next_y < 0:
                        next_face, next_heading = links[face][heading]
                        next_x, next_y = {
                            EAST: (0, next_x),
                            SOUTH: (self.face_size - next_x - 1, 0),
                            WEST: (self.face_size - 1, self.face_size - next_x - 1),
                            NORTH: (next_x, self.face_size - 1),
                        }[next_heading]
                if self.faces[next_face][next_y][next_x] == "#":
                    break
                face, x, y, heading = (next_face, next_x, next_y, next_heading)
                steps -= 1

        offset_x, offset_y = self.layout[face]
        x, y = offset_x * self.face_size + x, offset_y * self.face_size + y
        return 1000 * (y + 1) + 4 * (x + 1) + heading


def solve(inputs: str) -> None:
    map_data, instructions = inputs.split("\n\n")
    board = ForceFieldBoard(map_data)

    print(f"Part 1: {board.navigate_path(instructions)}")
    print(f"Part 2: {board.navigate_path(instructions, as_cube=True)}\n")


solve(sample_input)
solve(actual_input)
