"""https://adventofcode.com/2021/day/19"""
# import logging
import math
import os
import re
import string

from collections import defaultdict, Counter, deque
from itertools import combinations, product

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day19.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()

sample_input = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

DIRECTIONS = 2
ORIENTATIONS = 3
ROTATIONS = 4


class Scanner:
    def __init__(self, id: int, readings_data: str) -> None:
        self.id = id
        self._readings = [tuple(map(int, r.split(","))) for r in readings_data]
        self._origin = (0, 0, 0)

    def __repr__(self) -> str:
        return f"Scanner {self.id} @ {self._origin}"

    @property
    def beacons(self):
        x0, y0, z0 = self._origin
        return set((x0 + x, y0 + y, z0 + z) for x, y, z in self._readings)

    def set_origin(self, xyz):
        self._origin = xyz

    def reorient(self):
        self._readings = [(y, z, x) for x, y, z in self._readings]

    def switch_direction(self):
        self._readings = [(x, -y, -z) for x, y, z in self._readings]

    def rotate(self):
        self._readings = [(-y, x, z) for x, y, z in self._readings]

    def orient_to_field(self, beacon_field):
        for _ in range(ORIENTATIONS):
            for _ in range(DIRECTIONS):
                for _ in range(ROTATIONS):
                    for (x, y, z), (bx, by, bz) in product(self.beacons, beacon_field):
                        self.set_origin((bx - x, by - y, bz - z))
                        if self.aligned(beacon_field):
                            return True
                    self.set_origin((0, 0, 0))
                    self.rotate()
                self.switch_direction()
            self.reorient()
        return False

    def aligned(self, beacon_field):
        matching_beacons = self.beacons.intersection(beacon_field)
        return len(matching_beacons) >= 12


class ScannerOriented(Exception):
    """Used to break out of search when a scanner has matched"""


@print_time_taken
def solve(inputs):

    scanners = [
        Scanner(i, lines.splitlines()[1:])
        for i, lines in enumerate(inputs.split("\n\n"))
    ]

    unoriented_scanners = set(scanners[1:])
    beacon_field = scanners[0].beacons
    while unoriented_scanners:
        # Try and match an unoriented scanner to the current beacon field
        try:
            for scanner in unoriented_scanners:
                if scanner.orient_to_field(beacon_field):
                    raise ScannerOriented
            raise ValueError("No matching scanner found")
        except ScannerOriented:
            beacon_field |= scanner.beacons
            unoriented_scanners.remove(scanner)

    print(f"Part 1: {len(beacon_field)}")

    max_distance = 0
    for scanner1, scanner2 in combinations(scanners, 2):
        distance = sum(abs(a - b) for a, b in zip(scanner1._origin, scanner2._origin))
        max_distance = max(distance, max_distance)
    print(f"Part 2: {max_distance}\n")


solve(sample_input)
# solve(actual_input)
