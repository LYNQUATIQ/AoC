import os

from utils import flatten, print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day08_input.txt")) as f:
    actual_input = f.read()

sample_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


UNIQUE_LENGTHS = {2: 1, 3: 7, 4: 4, 7: 8}


def decode(patterns, outputs):
    answers = {}

    # Find 1, 4, 7 and 8
    for pattern in (p for p in patterns if len(p) in UNIQUE_LENGTHS):
        answers[UNIQUE_LENGTHS[len(pattern)]] = pattern

    # Find 0, 6 and 9
    for pattern in (p for p in patterns if len(p) == 6):
        if answers[4].issubset(pattern):
            answers[9] = pattern
        elif answers[1].issubset(pattern):
            answers[0] = pattern
        else:
            answers[6] = pattern

    # Find 2, 3 and 5
    for pattern in (p for p in patterns if len(p) == 5):
        if answers[1].issubset(pattern):
            answers[3] = pattern
        elif pattern.issubset(answers[6]):
            answers[5] = pattern
        else:
            answers[2] = pattern

    decoder = {v: str(k) for k, v in answers.items()}
    return int("".join(decoder[v] for v in outputs))


@print_time_taken
def solve(inputs):
    patterns, outputs = [], []
    for pattern, output in map(lambda x: x.split(" | "), inputs.splitlines()):
        patterns.append(list(map(frozenset, pattern.split())))
        outputs.append(list(map(frozenset, output.split())))

    print(f"Part 1: {sum(len(v) in UNIQUE_LENGTHS for v in flatten(outputs))}")
    print(f"Part 2: {sum(decode(a, b) for a, b in zip(patterns, outputs))}\n")


solve(sample_input)
solve(actual_input)
