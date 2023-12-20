"""https://adventofcode.com/2023/day/20"""
import os

from collections import defaultdict, deque

with open(os.path.join(os.path.dirname(__file__), "inputs/day20_input.txt")) as f:
    actual_input = f.read()


sample_input = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

sample_input = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

FLIPFLOP = "%"
CONJUNCTION = "&"
BROADCASTER, OUTPUT = "broadcaster", "output"

HIGH, LOW = True, False
ON, OFF = True, False


def button_press(module_destinations, module_inputs, conjunctions, flipflops, counts):
    pulses = deque([(None, LOW, BROADCASTER)])
    counts[LOW] += 1
    while pulses:
        sender, pulse, receiver = pulses.popleft()
        if receiver == "rx":
            if pulse == LOW:
                return False
            continue
        pulse_to_send = None
        if receiver == BROADCASTER:
            pulse_to_send = pulse
        if receiver in flipflops:
            if pulse != HIGH:
                state = not flipflops[receiver]
                flipflops[receiver] = state
                pulse_to_send = state
        if receiver in conjunctions:
            received = conjunctions[receiver]
            received[sender] = pulse
            pulse_to_send = HIGH
            if all(received[i] == HIGH for i in module_inputs[receiver]):
                pulse_to_send = LOW
        if pulse_to_send is not None:
            for destination in module_destinations[receiver]:
                counts[pulse_to_send] += 1
                pulses.append((receiver, pulse_to_send, destination))
    return True


def solve(inputs: str, test_rx: bool = False):
    module_destinations: dict[list[str]] = {OUTPUT: []}
    module_inputs: dict[str, set[str]] = defaultdict(set)
    conjunctions: dict[dict[str, bool]] = {}
    flipflops = {}
    for line in inputs.splitlines():
        module, destinations_list = line.split(" -> ")
        destinations = list(destinations_list.split(", "))
        module_type = module[0]
        if module_type in (FLIPFLOP, CONJUNCTION):
            module = module[1:]
            if module_type == FLIPFLOP:
                flipflops[module] = LOW
            else:
                conjunctions[module] = defaultdict(bool)
        module_destinations[module] = destinations
        for destination in destinations:
            module_inputs[destination].add(module)

    counts = {LOW: 0, HIGH: 0}
    for _ in range(1000):
        button_press(
            module_destinations, module_inputs, conjunctions, flipflops, counts
        )
    print(f"\nPart 1: {counts[LOW] * counts[HIGH]}")

    if not test_rx:
        return

    flipflops = {f: LOW for f in flipflops}
    conjunctions = {c: defaultdict(bool) for c in conjunctions}
    button_presses = 1
    while button_press(
        module_destinations, module_inputs, conjunctions, flipflops, counts
    ):
        button_presses += 1
        if button_presses % 1000 == 0:
            print(button_presses)

    print(f"Part 2: {button_presses}\n")


solve(sample_input)
solve(actual_input, test_rx=True)
