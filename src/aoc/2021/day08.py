"""https://adventofcode.com/2021/day/8"""

import os
from itertools import chain

with open(os.path.join(os.path.dirname(__file__), "inputs/day08_input.txt")) as f:
    actual_input = f.read()

example_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


UNIQUE = {2: "1", 3: "7", 4: "4", 7: "8"}


def decode(patterns, values):
    coding = {}

    # Find 1, 4, 7 and 8
    for pattern in (p for p in patterns if len(p) in UNIQUE):
        coding[UNIQUE[len(pattern)]] = pattern

    # Find 0, 6 and 9
    for pattern in (p for p in patterns if len(p) == 6):
        if coding["4"].issubset(pattern):
            coding["9"] = pattern
        elif coding["1"].issubset(pattern):
            coding["0"] = pattern
        else:
            coding["6"] = pattern

    # Find 2, 3 and 5
    for pattern in (p for p in patterns if len(p) == 5):
        if coding["1"].issubset(pattern):
            coding["3"] = pattern
        elif pattern.issubset(coding["6"]):
            coding["5"] = pattern
        else:
            coding["2"] = pattern

    decoder = {value: pattern for pattern, value in coding.items()}
    return int("".join(decoder[value] for value in values))


def solve(inputs):
    patterns, values = [], []
    for pattern, value in map(lambda x: x.split("|"), inputs.splitlines()):
        patterns.append(tuple(map(frozenset, pattern.split())))
        values.append(tuple(map(frozenset, value.split())))

    print(f"Part 1: {sum(len(v) in UNIQUE for v in chain.from_iterable(values))}")
    print(f"Part 2: {sum(decode(p, v) for p, v in zip(patterns, values))}\n")


solve(example_input)
solve(actual_input)
