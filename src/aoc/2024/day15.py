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


def draw_map(robot_xy, walls, boxes, width, height, big_boxes: bool = False):
    for y in range(height):
        x = 0
        while x < width - 1:
            xy = complex(x, y)
            x += 1
            if xy == robot_xy:
                print(ROBOT, end="")
            elif xy in boxes:
                if big_boxes:
                    print(BIG_BOX, end="")
                    x += 1
                else:
                    print(BOX, end="")
            elif xy in walls:
                print(WALL, end="")
            else:
                print(".", end="")
        print()


def solve(inputs: str):
    grid, instructions = inputs.split("\n\n")

    # walls, boxes = set(), set()
    # robot_xy = None
    # for y, row in enumerate(grid.split("\n")):
    #     for x, cell in enumerate(row):
    #         xy = complex(x, y)
    #         if cell == ROBOT:
    #             robot_xy = xy
    #         elif cell == WALL:
    #             walls.add(xy)
    #         elif cell == BOX:
    #             boxes.add(xy)
    # assert robot_xy is not None

    # for instruction in instructions:
    #     move = INSTRUCTIONS[instruction]
    #     xy = robot_xy + move
    #     boxes_to_move = []
    #     while xy in boxes:
    #         boxes_to_move.append(xy)
    #         xy += move
    #     if xy in walls:
    #         continue
    #     for box in boxes_to_move[::-1]:
    #         boxes.discard(box)
    #         boxes.add(box + move)
    #     robot_xy += move

    # gps_sum = 0
    # for box in boxes:
    #     gps_sum += abs(box.real) + abs(box.imag) * 100
    # print(f"Part 1: {int(gps_sum)}")

    walls, boxes_lhs = set(), set()
    robot_xy = None
    for y, row in enumerate(grid.split("\n")):
        x = 0
        for _, cell in enumerate(row):
            xy = complex(x, y)
            next_xy = complex(x + 1, y)
            x += 2
            if cell == ROBOT:
                robot_xy = xy
            elif cell == WALL:
                walls.add(xy)
                walls.add(next_xy)
            elif cell == BOX:
                boxes_lhs.add(xy)

    iteration = 0
    for instruction in instructions:
        connected_boxes = {box: box + RIGHT for box in boxes_lhs}
        connected_boxes |= {v: k for k, v in connected_boxes.items()}
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
            if move in (UP, DOWN):
                front_edge |= {connected_boxes[edge] for edge in front_edge}
            boxes_to_move |= front_edge
            front_edge = {edge + move for edge in front_edge}

        if not hit_wall:
            robot_xy += move
            boxes_to_move &= boxes_lhs
            boxes_lhs -= boxes_to_move
            boxes_lhs |= {box + move for box in boxes_to_move}

    gps_sum = 0
    for box in boxes_lhs:
        gps_sum += abs(box.real) + abs(box.imag) * 100
    print(f"Part 2: {int(gps_sum)}\n")


solve(example_input)
solve(actual_input)
