import os
import re

from itertools import product

from utils import flatten, print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day19_input.txt")) as f:
    actual_input = f.read()

sample_input = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


def get_patterns(rules_input):
    matched, unmatched = {}, {}
    for line in rules_input:
        i, rule = line.split(": ")
        if rule[1] in "ab":
            matched[int(i)] = rule[1]
            continue
        unmatched[int(i)] = tuple([int(x) for x in x.split()] for x in rule.split("| "))

    while unmatched:
        patterns, candidate_id = None, None
        for candidate_id, rule in unmatched.items():
            if not any(i not in matched for i in list(flatten(rule))):
                patterns = set()
                for r in rule:
                    combos = (matched[n] for n in r)
                    patterns.update("".join(combo) for combo in product(*combos))
                break
        matched[candidate_id] = patterns
        del unmatched[candidate_id]

    return matched


@print_time_taken
def solve(inputs):
    rules, messages = map(lambda x: x.splitlines(), inputs.split("\n\n"))

    patterns = get_patterns(rules)
    print(f"Part 1: {sum(p in patterns[0] for p in messages)}")

    regex42 = re.compile(r"^(" + "|".join(patterns[42]) + r"){2,}")
    regex31 = re.compile(r"^(" + "|".join(patterns[31]) + r")+$")
    part2 = 0
    for message in (m for m in messages if regex42.match(m)):
        m42 = regex42.match(message).group(0)
        if len(m42) <= len(message) // 2:
            continue
        if regex31.match(message.replace(m42, "")):
            part2 += 1
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
