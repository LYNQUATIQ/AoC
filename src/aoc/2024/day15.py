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

# example_input = """#######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^"""

WALL, BOX, ROBOT = "#", "O", "@"
BOX_LHS, BOX_RHS, BIG_BOX = "[", "]", "[]"

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

    walls, boxes, connected_boxes, boxes_lhs = set(), set(), {}, set()
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
                boxes.add(xy)
                boxes.add(next_xy)
                connected_boxes[xy] = next_xy
                connected_boxes[next_xy] = xy
    width, height = x + 1, y + 1
    iteration = 0
    for instruction in instructions:
        iteration += 1
        move = INSTRUCTIONS[instruction]
        xy = robot_xy + move
        hit_wall = False
        if move in (LEFT, RIGHT):
            boxes_to_move = set()
            while xy in boxes:
                boxes_to_move.add(xy)
                xy += move
            if xy in walls:
                hit_wall = True
                continue
        elif move in (UP, DOWN):
            boxes_to_move, front_edge = set(), {xy}
            hit_wall = False
            while front_edge:
                if any(edge in walls for edge in front_edge):
                    hit_wall = True
                    break
                front_edge = {edge for edge in front_edge if edge in boxes}
                front_edge |= {connected_boxes[edge] for edge in front_edge}
                boxes_to_move |= front_edge
                front_edge = {edge + move for edge in front_edge}

        if not hit_wall:
            robot_xy += move
            boxes -= boxes_to_move
            boxes |= {box + move for box in boxes_to_move}
            new_connected_boxes = {
                box + move: connected_boxes[box] + move for box in boxes_to_move
            }
            for box in boxes_to_move:
                connected_boxes.pop(box)
            connected_boxes |= new_connected_boxes
            new_lhs = {box + move for box in boxes_to_move if box in boxes_lhs}
            boxes_lhs -= boxes_to_move
            boxes_lhs |= new_lhs

        print("Move", instruction)
        draw_map(robot_xy, walls, boxes, width, height, big_boxes=True)
        print(iteration)
    gps_sum = 0
    for box in boxes_lhs:
        gps_sum += abs(box.real) + abs(box.imag) * 100
    print(f"Part 2: {gps_sum}\n")


solve(example_input)
solve(actual_input)
