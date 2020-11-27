import logging
import os
import math

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


player_ratings = {}

for line in lines:
    a, b, result = line.split(",")
    sa, sb = result.split("-")
    sa, sb = int(sa), int(sb)
    ra = player_ratings.get(a, 1200)
    rb = player_ratings.get(b, 1200)
    print(f"{a}({ra:.3f}) playing {b}({rb:.3f}) - score: {sa}-{sb}", end="")
    if sa > sb:
        e = 1 / (1 + 10 ** ((rb - ra) / 400))
        d = 20 * (1 - e)
        player_ratings[a] = ra + d
        player_ratings[b] = rb - d
    else:
        e = 1 / (1 + 10 ** ((ra - rb) / 400))
        d = 20 * (1 - e)
        player_ratings[a] = ra - d
        player_ratings[b] = rb + d
    print(f"    rating change: +/-{d:.3f}")

max_elo = max(player_ratings.values())
min_elo = min(player_ratings.values())
for k, v in player_ratings.items():
    print(f"{k:>15}: {v:.3f}  ", end="")
    s = ""
    if v == max_elo:
        s = "<- MAX"
    if v == min_elo:
        s = "<- MIN"
    print(s)
print(math.floor(max_elo) - math.floor(min_elo))
