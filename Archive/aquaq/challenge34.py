import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

trains = lines[0].split(",")[1:]
time_taken = {}

# stations_with_trains - station: (train, depart_time)
stations_with_trains = {}

# trains_queuing - station: {train: (arrival_time, previous_station)}
trains_queuing = defaultdict(dict)

# trains_en_route - train: (arrival_time, next_station, previous_station)
trains_en_route = {}


timetable = defaultdict(list)
last_departure_time = {train: 0 for train in trains}
for line in lines[1:]:
    tokens = line.split(",")
    station = tokens[0]
    for train, time in zip(trains, tokens[1:]):
        if time:
            hh, mm = time.split(":")
            arrival_time = int(hh) * 60 + int(mm)
            journey_time = arrival_time - last_departure_time[train]
            last_departure_time[train] = arrival_time
            timetable[train].append((station, journey_time))

for train in trains:
    station, time = timetable[train].pop(0)
    trains_en_route[train] = (time, station, " ")

t = 0
while trains_en_route or stations_with_trains or trains_queuing:
    t += 1

    # Check if any trains in station can depart
    departed = []
    for station, (train, depart_time) in stations_with_trains.items():
        if depart_time == t:
            departed.append(station)
            try:
                next_station, journey_time = timetable[train].pop(0)
                trains_en_route[train] = (t + journey_time, next_station, station)
                print(f"{t//60:02}:{t%60:02} - {train} departs {station}")
            except IndexError:
                # Completed journey
                time_taken[train] = t - time_taken[train]
                print(
                    f"{t//60:02}:{t%60:02} - {train} departs {station} completing its journey"
                )
    for station in departed:
        del stations_with_trains[station]

    # Check if any trains en route have arrived
    arrived = []
    for train, (arrival_time, station, previous_station) in trains_en_route.items():
        if arrival_time == t:
            arrived.append(train)
            print(
                f"{t//60:02}:{t%60:02} - {train} arrives at {station} and joins queue"
            )
            trains_queuing[station][train] = (arrival_time, previous_station)
            if train not in time_taken:
                time_taken[train] = t
    for train in arrived:
        del trains_en_route[train]

    # Check if any trains can move from the queue into the station
    empty_queues = []
    for station, queue in trains_queuing.items():
        if queue and station not in stations_with_trains:
            q = sorted([(s, a, t) for t, (a, s) in queue.items()])
            _, _, train = q[0]
            del queue[train]
            if not queue:
                empty_queues.append(station)
            stations_with_trains[station] = (train, t + 5)
            print(f"{t//60:02}:{t%60:02} - {train} moves to platform at {station}")
    for station in empty_queues:
        del trains_queuing[station]

print(max(time_taken.values()))
