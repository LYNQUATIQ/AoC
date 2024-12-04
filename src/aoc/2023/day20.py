import os

from collections import defaultdict, deque
import math

with open(os.path.join(os.path.dirname(__file__), "inputs/day20_input.txt")) as f:
    actual_input = f.read()


example_input = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

FLIPFLOP = "%"
CONJUNCTION = "&"
BROADCASTER, OUTPUT = "broadcaster", "output"

HIGH, LOW = True, False
ON, OFF = True, False

BIT_ORDER = {
    "sn": {"ng": 1, "vp": 2, "vf": 4, "bt": 256, "xd": 512, "tn": 1024, "tv": 2048},
    "tf": {"gr": 1, "td": 16, "vr": 64, "hq": 128, "mq": 512, "fl": 1024, "gz": 2048},
    "lr": {"js": 1, "xv": 8, "hj": 32, "hm": 256, "rd": 512, "xl": 1024, "gx": 2048},
    "hl": {"lb": 1, "qk": 16, "hs": 32, "xb": 128, "kg": 512, "px": 1024, "tm": 2048},
}

BLOCKS = {True: "\u2588", False: "\u25af"}


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


def solve(inputs: str, analyse_inputs: bool = False):
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

    if not analyse_inputs:
        return

    flipflops = {f: LOW for f in flipflops}
    conjunctions = {c: defaultdict(bool) for c in conjunctions}
    presses = 0
    while presses < 2_500:
        presses += 1
        button_press(
            module_destinations, module_inputs, conjunctions, flipflops, counts
        )
        m = "lr"
        print(
            presses,
            ", ".join(f"{k}-{BLOCKS[conjunctions[m].get(k, 0)]}" for k in BIT_ORDER[m]),
        )

    print(f"\nPart 2: {math.lcm(*[sum(BIT_ORDER[m].values()) for m in BIT_ORDER])}\n")


solve(example_input)
solve(actual_input, analyse_inputs=True)
