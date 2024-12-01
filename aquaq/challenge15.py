import logging
import os
import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

dictionary = defaultdict(list)

input_file = os.path.join(script_dir, f"inputs/words.txt")
for word in open(input_file):
    word = word.rstrip("\n")
    l = len(word)
    if l >= 3 and l <= 6:
        dictionary[l].append(word)


def find_ladder(start, target):
    def find_words_one_away(start, already_seen):
        words = set()
        for i in range(n_letters):
            current_letter = start[i]
            for c in string.ascii_lowercase:
                candidate = start[:i] + c + start[i + 1 :]
                if candidate not in already_seen and candidate in valid_words:
                    words.add(candidate)
        return words

    n_letters = len(start)
    valid_words = dictionary[n_letters]
    ladder = {start: None}
    already_seen = {start}
    current_rung = [start]
    while target not in ladder:
        next_rung = []
        for current_word in current_rung:
            words_one_away = find_words_one_away(current_word, already_seen)
            for next_word in words_one_away:
                ladder[next_word] = current_word
                already_seen.add(next_word)
            next_rung += words_one_away
        current_rung = next_rung

    # Work back through destinations in shortest path
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = ladder[step]
    path = path[::-1]

    return path


word_pairs = [
    ("dog", "war"),
    ("bow", "ply"),
    ("tree", "fled"),
    ("fire", "park"),
    ("forge", "house"),
    ("stall", "chili"),
    ("start", "great"),
    ("inner", "outer"),
    ("asking", "bobble"),
    ("coffee", "drawer"),
]
answer = 1
for start, target in word_pairs:
    print(f" Calculating {start}->{target}...", end="")
    path = find_ladder(start, target)
    print(path)
    answer *= len(path)
print(answer)
