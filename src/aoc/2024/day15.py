"""https://adventofcode.com/2024/day/15"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 15)
example_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


WALL, BOX, ROBOT, BIG_BOX = "#", "O", "@", "[]"
UP, DOWN, LEFT, RIGHT = -1j, 1j, -1, 1
INSTRUCTIONS = {"^": UP, ">": RIGHT, "v": DOWN, "<": LEFT, "\n": 0}


def sum_box_gps(inputs: str, big_boxes: bool = False):
    grid, instructions = inputs.split("\n\n")

    walls, boxes = set(), set()
    robot_xy = None
    for y, row in enumerate(grid.split("\n")):
        x = 0
        for _, cell in enumerate(row):
            xy = complex(x, y)
            if cell == ROBOT:
                robot_xy = xy
            elif cell == WALL:
                walls.add(xy)
            elif cell == BOX:
                boxes.add(xy)
            if big_boxes:
                x += 1
                if cell == WALL:
                    walls.add(xy + RIGHT)
            x += 1

    iteration = 0
    for instruction in instructions:
        if big_boxes:
            connected_boxes = {box: box + RIGHT for box in boxes}
            connected_boxes |= {v: k for k, v in connected_boxes.items()}
        else:
            connected_boxes = boxes
        iteration += 1
        move = INSTRUCTIONS[instruction]
        xy = robot_xy + move
        hit_wall = False
        boxes_to_move, front_edge = set(), {xy}
        hit_wall = False
        while front_edge:
            if any(edge in walls for edge in front_edge):
                hit_wall = True
                break
            front_edge = {edge for edge in front_edge if edge in connected_boxes}
            if big_boxes and move in (UP, DOWN):
                front_edge |= {connected_boxes[edge] for edge in front_edge}
            boxes_to_move |= front_edge
            front_edge = {edge + move for edge in front_edge}

        if not hit_wall:
            robot_xy += move
            boxes_to_move &= boxes
            boxes -= boxes_to_move
            boxes |= {box + move for box in boxes_to_move}

    gps_sum = 0
    for box in boxes:
        gps_sum += int(abs(box.real) + abs(box.imag) * 100)
    return gps_sum


def solve(inputs: str):
    print(f"Part 1: {sum_box_gps(inputs)}")
    print(f"Part 2: {sum_box_gps(inputs, big_boxes=True)}\n")


solve(example_input)
solve(actual_input)
