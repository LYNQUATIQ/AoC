import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
line = lines[0]


class Face:

    CLOCKWISE_ROTATION = {0: 6, 1: 3, 2: 0, 3: 7, 4: 4, 5: 1, 6: 8, 7: 5, 8: 2}
    COUNTER_CLOCKWISE_ROTATION = {0: 2, 1: 5, 2: 8, 3: 1, 4: 4, 5: 7, 6: 0, 7: 3, 8: 6}

    SYMBOLS = {
        0: ("┌──", "| x", "|  "),
        1: ("───", " x ", "   "),
        2: ("──┐", "x |", "  |"),
        3: ("|  ", "| x", "|  "),
        4: ("   ", " x ", "   "),
        5: ("  |", "x |", "  |"),
        6: ("|  ", "| x", "└──"),
        7: ("   ", " x ", "───"),
        8: ("  |", "x |", "──┘"),
    }

    def __init__(self, face_value):
        self.face_values = {i: f"{face_value}{str(i)}" for i in range(9)}

    def __str__(self):
        return "\n".join([self.row(i, " ") for i in [1, 2, 3]])

    def row(self, row, spacer=" "):
        i = (row - 1) * 3
        return spacer.join([str(self.face_values[i]) for i in range(i, i + 3)])

    def get_face_values(self, indices):
        return [self.face_values[i] for i in indices]

    def set_face_values(self, indices, values):
        for i, v in zip(indices, values):
            self.face_values[i] = v

    def rotate(self, counter_clockwise=False):
        if counter_clockwise:
            rotation = self.COUNTER_CLOCKWISE_ROTATION
        else:
            rotation = self.CLOCKWISE_ROTATION
        self.face_values = {k: self.face_values[v] for k, v in rotation.items()}


class RubiksCube:

    FRONT_FACE = 1
    UP_FACE = 2
    LEFT_FACE = 3
    RIGHT_FACE = 4
    DOWN_FACE = 5
    BACK_FACE = 6

    TOP_EDGE = "Top"
    LEFT_EDGE = "Left"
    BOTTOM_EDGE = "Bottom"
    RIGHT_EDGE = "Right"

    FACE_CHAR_MAP = {
        "F": FRONT_FACE,
        "U": UP_FACE,
        "L": LEFT_FACE,
        "R": RIGHT_FACE,
        "D": DOWN_FACE,
        "B": BACK_FACE,
    }

    # Top, right, bottom, left
    EDGES = {
        FRONT_FACE: {
            TOP_EDGE: (UP_FACE, [6, 7, 8]),
            RIGHT_EDGE: (RIGHT_FACE, [0, 3, 6]),
            BOTTOM_EDGE: (DOWN_FACE, [2, 1, 0]),
            LEFT_EDGE: (LEFT_FACE, [8, 5, 2]),
        },
        UP_FACE: {
            TOP_EDGE: (BACK_FACE, [6, 7, 8]),
            RIGHT_EDGE: (RIGHT_FACE, [2, 1, 0]),
            BOTTOM_EDGE: (FRONT_FACE, [2, 1, 0]),
            LEFT_EDGE: (LEFT_FACE, [2, 1, 0]),
        },
        LEFT_FACE: {
            TOP_EDGE: (UP_FACE, [0, 3, 6]),
            RIGHT_EDGE: (FRONT_FACE, [0, 3, 6]),
            BOTTOM_EDGE: (DOWN_FACE, [0, 3, 6]),
            LEFT_EDGE: (BACK_FACE, [0, 3, 6]),
        },
        RIGHT_FACE: {
            TOP_EDGE: (UP_FACE, [8, 5, 2]),
            RIGHT_EDGE: (BACK_FACE, [8, 5, 2]),
            BOTTOM_EDGE: (DOWN_FACE, [8, 5, 2]),
            LEFT_EDGE: (FRONT_FACE, [8, 5, 2]),
        },
        DOWN_FACE: {
            TOP_EDGE: (FRONT_FACE, [6, 7, 8]),
            RIGHT_EDGE: (RIGHT_FACE, [6, 7, 8]),
            BOTTOM_EDGE: (BACK_FACE, [2, 1, 0]),
            LEFT_EDGE: (LEFT_FACE, [6, 7, 8]),
        },
        BACK_FACE: {
            TOP_EDGE: (DOWN_FACE, [6, 7, 8]),
            RIGHT_EDGE: (RIGHT_FACE, [8, 5, 2]),
            BOTTOM_EDGE: (UP_FACE, [2, 1, 0]),
            LEFT_EDGE: (LEFT_FACE, [0, 3, 6]),
        },
    }

    def __init__(self):
        self.faces = {
            self.FACE_CHAR_MAP[f]: Face(f) for f in "FULRDB"
        }  # self.FACE_CHAR_MAP.values()}

    def rotate(self, face_char, counter_clockwise=False):
        face = self.FACE_CHAR_MAP[face_char]
        direction = -1 if counter_clockwise else 1
        connected_faces = self.EDGES[face]
        edge_values = {
            edge: self.faces[f].get_face_values(e)
            for edge, (f, e) in connected_faces.items()
        }
        edges = list(connected_faces)
        edge_map = {edges[i]: edges[(i + direction) % 4] for i in range(4)}
        for old_edge, new_edge in edge_map.items():
            f, e = connected_faces[new_edge]
            self.faces[f].set_face_values(e, edge_values[old_edge])
        self.faces[face].rotate(counter_clockwise)

    def print_cube(self, title=""):
        print("_" * 30 + "\n" + title)
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["U"]].row(1))
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["U"]].row(2))
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["U"]].row(3))
        print(" " * 13 + "U")
        print()
        print(
            self.faces[self.FACE_CHAR_MAP["L"]].row(1)
            + "  "
            + self.faces[self.FACE_CHAR_MAP["F"]].row(1)
            + "  "
            + self.faces[self.FACE_CHAR_MAP["R"]].row(1)
        )
        print(
            self.faces[self.FACE_CHAR_MAP["L"]].row(2)
            + "  "
            + self.faces[self.FACE_CHAR_MAP["F"]].row(2)
            + "  "
            + self.faces[self.FACE_CHAR_MAP["R"]].row(2)
        )
        print(
            self.faces[self.FACE_CHAR_MAP["L"]].row(3)
            + "  "
            + self.faces[self.FACE_CHAR_MAP["F"]].row(3)
            + "  "
            + self.faces[self.FACE_CHAR_MAP["R"]].row(3)
        )
        print("   L         F         R")
        print()
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["D"]].row(1))
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["D"]].row(2))
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["D"]].row(3))
        print(" " * 13 + "D")
        print()
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["B"]].row(1))
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["B"]].row(2))
        print(" " * 10 + self.faces[self.FACE_CHAR_MAP["B"]].row(3))
        print(" " * 13 + "B")
        print()


cube = RubiksCube()
cube.print_cube()
# line = "U'LBRU"

i = 0
while i < len(line):
    face = line[i]
    i += 1
    counter_clockwise = False
    try:
        if line[i] == "'":
            counter_clockwise = True
            i += 1
    except IndexError:
        pass
    cube.rotate(face, counter_clockwise)
    # cube.print_cube(f"Rotate {face} {'counter-' if counter_clockwise else ''}clockwise")

answer = 1
for n in cube.faces[cube.FRONT_FACE].face_values.values():
    answer *= cube.FACE_CHAR_MAP[n[0]]
print(answer)
cube.print_cube()
