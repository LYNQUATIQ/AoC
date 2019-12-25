import logging
import os


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_24_log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)


class Eris:

    SPACE = "."
    BUG = "#"

    """
                7

          0  1  2  3  4
          5  6  7  8  9
    11    10 11    13 14   13
          15 16 17 18 19
          20 21 22 23 24

                17
    """
    recursive_neighbours = {
        0: [(7, +1), (1, 0), (5, 0), (11, +1)],
        1: [(7, +1), (2, 0), (6, 0), (0, 0)],
        2: [(7, +1), (3, 0), (7, 0), (1, 0)],
        3: [(7, +1), (4, 0), (8, 0), (2, 0)],
        4: [(7, +1), (13, +1), (9, 0), (3, 0)],
        #
        5: [(0, 0), (6, 0), (10, 0), (11, +1)],
        6: [(1, 0), (7, 0), (11, 0), (5, 0)],
        7: [(2, 0), (8, 0), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (6, 0)],
        8: [(3, 0), (9, 0), (13, 0), (7, 0)],
        9: [(4, 0), (13, +1), (14, 0), (8, 0)],
        #
        10: [(5, 0), (11, 0), (15, 0), (11, +1)],
        11: [(6, 0), (0, -1), (5, -1), (10, -1), (15, -1), (20, -1), (16, 0), (10, 0)],
        #
        13: [(8, 0), (14, 0), (18, 0), (4, -1), (9, -1), (14, -1), (19, -1), (24, -1),],
        14: [(9, 0), (13, +1), (19, 0), (13, 0)],
        #
        15: [(10, 0), (16, 0), (20, 0), (11, +1)],
        16: [(11, 0), (17, 0), (21, 0), (15, 0)],
        17: [
            (20, -1),
            (21, -1),
            (22, -1),
            (23, -1),
            (24, -1),
            (18, 0),
            (22, 0),
            (16, 0),
        ],
        18: [(13, 0), (19, 0), (23, 0), (17, 0)],
        19: [(14, 0), (13, +1), (24, 0), (18, 0)],
        #
        20: [(15, 0), (21, 0), (17, +1), (11, +1)],
        21: [(16, 0), (22, 0), (17, +1), (20, 0)],
        22: [(17, 0), (23, 0), (17, +1), (21, 0)],
        23: [(18, 0), (24, 0), (17, +1), (22, 0)],
        24: [(19, 0), (13, +1), (17, +1), (23, 0)],
    }

    non_recursive_neighbours = {
        0: [(1, 0), (5, 0),],
        1: [(2, 0), (6, 0), (0, 0)],
        2: [(3, 0), (7, 0), (1, 0)],
        3: [(4, 0), (8, 0), (2, 0)],
        4: [(9, 0), (3, 0)],
        #
        5: [(0, 0), (6, 0), (10, 0),],
        6: [(1, 0), (7, 0), (11, 0), (5, 0)],
        7: [(2, 0), (8, 0), (12, 0), (6, 0)],
        8: [(3, 0), (9, 0), (13, 0), (7, 0)],
        9: [(4, 0), (14, 0), (8, 0)],
        #
        10: [(5, 0), (11, 0), (15, 0),],
        11: [(6, 0), (12, 0), (16, 0), (10, 0)],
        12: [(7, 0), (13, 0), (17, 0), (11, 0)],
        13: [(8, 0), (14, 0), (18, 0), (12, 0),],
        14: [(9, 0), (19, 0), (13, 0)],
        #
        15: [(10, 0), (16, 0), (20, 0),],
        16: [(11, 0), (17, 0), (21, 0), (15, 0)],
        17: [(12, 0), (18, 0), (22, 0), (16, 0),],
        18: [(13, 0), (19, 0), (23, 0), (17, 0)],
        19: [(14, 0), (24, 0), (18, 0)],
        #
        20: [(15, 0), (21, 0),],
        21: [(16, 0), (22, 0), (20, 0)],
        22: [(17, 0), (23, 0), (21, 0)],
        23: [(18, 0), (24, 0), (22, 0)],
        24: [(19, 0), (23, 0)],
    }

    def __init__(self):
        initial_bugs = [0, 1, 3, 6, 7, 10, 11, 13, 16, 17, 18, 19, 20, 21, 22]
        # initial_bugs = [4, 5, 8, 10, 13, 14, 17, 20]
        self.bugs = set()
        for cell in initial_bugs:
            self.bugs.add((cell, 0))

    def neighbours(self, cell, level, recursion=True):
        if recursion:
            neighbours = self.recursive_neighbours
        else:
            neighbours = self.non_recursive_neighbours
        return [(c, level + o) for c, o in neighbours[cell]]

    def neighbouring_bugs(self, cell, level, recursion=True):
        return sum(n in self.bugs for n in self.neighbours(cell, level, recursion))

    def universe(self, recursion):
        universe = set()
        for cell, level in self.bugs:
            universe.add((cell, level))
            for neighbour in self.neighbours(cell, level, recursion):
                universe.add(neighbour)
        return universe

    def biodiversity(self):
        return sum(2 ** cell for cell, _ in self.bugs)

    def process_round(self, recursion=True):
        new_bugs = set()

        for cell, level in self.universe(recursion):
            has_bug = (cell, level) in self.bugs
            neighbouring_bugs = self.neighbouring_bugs(cell, level, recursion)
            if has_bug and neighbouring_bugs == 1:
                new_bugs.add((cell, level))
            if not has_bug and (neighbouring_bugs == 1 or neighbouring_bugs == 2):
                new_bugs.add((cell, level))

        self.bugs = new_bugs


eris = Eris()
biodiversities = set()
while True:
    eris.process_round(recursion=False)
    biodiversity = eris.biodiversity()
    if biodiversity in biodiversities:
        break
    biodiversities.add(biodiversity)
print(f"Part 1: {biodiversity}")

eris = Eris()
for _ in range(200):
    eris.process_round(recursion=True)
print(f"Part 2: {len(eris.bugs)}")
