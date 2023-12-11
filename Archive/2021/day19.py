"""https://adventofcode.com/2021/day/19"""
import os

from collections import Counter
from itertools import combinations, permutations, product


with open(os.path.join(os.path.dirname(__file__), "inputs/day19_input.txt")) as f:
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

DIRECTIONS = (+1, -1)
ORIENTATIONS = ("XYZ", "YZX", "ZXY")
ROTATIONS = (0, 90, 180, 270)


class Scanner:
    def __init__(self, readings_data: str) -> None:
        self.beacons = {tuple(map(int, r.split(","))) for r in readings_data}
        self.distances = Counter(
            (ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2
            for (ax, ay, az), (bx, by, bz) in permutations(self.beacons, 2)
        )
        self.position = (0, 0, 0)

    def offset_readings(self, offset):
        dx, dy, dz = offset
        return {(x + dx, y + dy, z + dz) for x, y, z in self.beacons}

    def set_position(self, position=None):
        self.position = position
        self.beacons = self.offset_readings(position)

    def reorient(self):
        self.beacons = {(y, z, x) for x, y, z in self.beacons}

    def switch_direction(self):
        self.beacons = {(x, -y, -z) for x, y, z in self.beacons}

    def rotate(self):
        self.beacons = {(-y, x, z) for x, y, z in self.beacons}

    def orient(self, other):
        if sum((self.distances & other.distances).values()) < 12:
            return
        for _ in ORIENTATIONS:
            for _ in DIRECTIONS:
                for _ in ROTATIONS:
                    for (x, y, z), (x0, y0, z0) in product(self.beacons, other.beacons):
                        offset = (x0 - x, y0 - y, z0 - z)
                        offset_readings = self.offset_readings(offset)
                        if len(offset_readings.intersection(other.beacons)) >= 12:
                            self.set_position(offset)
                            return True
                    self.rotate()
                self.switch_direction()
            self.reorient()
        return False


def solve(inputs):
    scanners = [Scanner(lines.splitlines()[1:]) for lines in inputs.split("\n\n")]

    oriented_scanners, unoriented_scanners = {scanners[0]}, set(scanners[1:])
    while unoriented_scanners:
        to_match = oriented_scanners.pop()
        matched_scanners = {s for s in unoriented_scanners if s.orient(to_match)}
        unoriented_scanners.difference_update(matched_scanners)
        oriented_scanners |= matched_scanners

    beacons = set().union(*[s.beacons for s in scanners])
    print(f"Part 1: {len(beacons)}")

    max_distance = 0
    for s1, s2 in combinations(scanners, 2):
        distance = sum(abs(a - b) for a, b in zip(s1.position, s2.position))
        max_distance = max(distance, max_distance)
    print(f"Part 2: {max_distance}\n")


solve(sample_input)
solve(actual_input)
