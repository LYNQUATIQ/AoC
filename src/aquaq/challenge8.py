import logging
import os
import datetime
import math

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

purchases = {}
first_date = None
for line in lines:
    yyyymmdd, m, c = line.split(",")
    yyyy, mm, dd = yyyymmdd.split("-")
    d = datetime.date(int(yyyy), int(mm), int(dd))
    purchases[d] = (int(m), int(c))
    if first_date is None:
        first_date = d
last_date = d

milk = defaultdict(int)
cereal = 0
current_date = first_date
while current_date <= last_date:
    m, c = purchases[current_date]

    # Add any cereal purchased
    cereal += c

    # Have breakfast
    had_breakfast = False
    if sum(milk.values()) >= 100 and cereal >= 100:
        milk[min(milk)] -= 100
        cereal -= 100
        had_breakfast = True

    # Throw away old milk
    old_milk = [k for k in milk if k <= current_date - datetime.timedelta(days=5)]
    for k in old_milk:
        del milk[k]

    # Add any milk purchased
    if m > 0:
        milk[current_date] = m

    p = f"   Purchased: {m}, {c}" if m + c > 0 else ""
    b = f"   Had breakfast :)  " if had_breakfast else "    No breakfast :(  "
    print(f"{current_date}   {sum(milk.values()):>6} {cereal:>6} {b} {p}")
    current_date += datetime.timedelta(days=1)

print(sum(milk.values()) + cereal)
