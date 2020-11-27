import logging
import os

import datetime

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

open_streaks = {}
longest_length = datetime.timedelta(0)
longest_streak = None


def process_result(team, goals, date):
    global longest_length, longest_streak
    if goals > 0:
        try:
            streak_start = open_streaks[team]
            del open_streaks[team]
            if (date - streak_start) > longest_length:
                longest_length = date - streak_start
                longest_streak = (team, streak_start, date)
        except KeyError:
            pass
    if goals == 0 and team not in open_streaks:
        open_streaks[team] = date


for line in lines[1:]:
    results = line.split(",")
    yyyymmdd = results[0]
    team_a = results[1]
    team_b = results[2]
    goals_a = int(results[3])
    goals_b = int(results[4])
    yyyy, mm, dd = map(int, yyyymmdd.split("-"))
    date = datetime.date(yyyy, mm, dd)
    process_result(team_a, goals_a, date)
    process_result(team_b, goals_b, date)

team, start, end = longest_streak
print(f"{team} {start.strftime('%Y%m%d')} {end.strftime('%Y%m%d')}")
