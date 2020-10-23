import logging
import os

import re
import string

from collections import Counter, defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

class IPV7:
    def __init__(self, supernet_seqs, hypernet_seqs):
        self.supernet_seqs = supernet_seqs
        self.hypernet_seqs = hypernet_seqs

    def support_tls(self):
        def contains_abba(token):
            if len(token) < 4:
                return False
            for i in range(len(token)-3):
                if token[i] == token[i+3] and token[i+1] == token[i+2] and token[i] != token[i+1]:
                    return True
            return False

        for token in self.hypernet_seqs:
            if contains_abba(token):
                return False

        for token in self.supernet_seqs:
            if contains_abba(token):
                return True

        return False

    def support_sls(self):
        def abas_in_token(token):
            if len(token) < 3:
                return []
            abas_in_token = []
            for i in range(len(token)-2):
                if token[i] == token[i+2] and token[i] != token[i+1]:
                    abas_in_token.append(token[i:i+3])
            return abas_in_token

        supernet_abas = []
        for token in self.supernet_seqs:
            supernet_abas.extend(abas_in_token(token))

        if not supernet_abas:
            return False

        reversed_abas = [aba[1]+aba[0]+aba[1] for aba in supernet_abas]
        for token in self.hypernet_seqs:
            for aba in abas_in_token(token):
                if aba in reversed_abas:
                    return True

        return False  


supports_tls = 0
supports_sls = 0
for line in lines:
    outside_brackets, inside_brackets = [], []
    p1 = 0
    p2 = line.find("[", p1)
    while p2 != -1:
        if p2 > p1:
            outside_brackets.append(line[p1:p2])
        p1 = p2 + 1
        p2 = line.find("]", p1)
        assert p2 != -1
        inside_brackets.append(line[p1:p2])
        p1 = p2 + 1
        p2 = line.find("[", p1)
    if p1 < len(line):
        outside_brackets.append(line[p1:])

    ipv7 = IPV7(outside_brackets, inside_brackets)
    if ipv7.support_tls():
        supports_tls += 1
    if ipv7.support_sls():
        supports_sls += 1

print(f"Part 1: {supports_tls}")
print(f"Part 2: {supports_sls}")






