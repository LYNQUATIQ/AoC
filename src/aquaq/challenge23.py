import logging
import os

import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

keyword = "powerplant"
coded_text = "vepcundbyoaeirotivluxnotpstfnbwept"

# keyword = "playfair"
# coded_text = "pabapgxyxy"

playfair = ""
for c in keyword + string.ascii_lowercase:
    if c not in playfair and c != "j":
        playfair += c

cypher = {}
reverse_cypher = {}
for y in range(5):
    for x in range(5):
        c = playfair[x + y * 5]
        print(c, end="")
        cypher[c] = (x, y)
        reverse_cypher[(x, y)] = c
    print("")

plaintext = ""
for i in range(0, len(coded_text), 2):
    l1 = coded_text[i]
    l2 = coded_text[i + 1]
    x1, y1 = cypher[l1]
    x2, y2 = cypher[l2]
    if x1 == x2:
        p1 = reverse_cypher[(x1, (y1 - 1) % 5)]
        p2 = reverse_cypher[(x2, (y2 - 1) % 5)]
    elif y1 == y2:
        p1 = reverse_cypher[((x1 - 1) % 5), y1]
        p2 = reverse_cypher[((x2 - 1) % 5), y2]
    else:
        p1 = reverse_cypher[x2, y1]
        p2 = reverse_cypher[x1, y2]
    plaintext += p1 + p2

    print(f"Decoding: {l1}{l2} -> {p1}{p2}")

print(plaintext)
