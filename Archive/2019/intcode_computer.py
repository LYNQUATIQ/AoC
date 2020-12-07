import logging

logging.basicConfig(
    level=logging.WARNING,
    filename="intcode_computer.log",
    filemode="w",
)


class IntCodeComputer:
    NOT_STARTED = "Not started"
    RUNNING = "Running"
    AWAITING_INPUT = "Awaiting input"
    TERMINATED = "Terminated"

    def __init__(self, program, memory_overrides={}):
        self.memory = {loc: code for loc, code in enumerate(program)}
        for i, override in memory_overrides.items():
            self.memory[i] = override
        self.input_values = []
        self.output_values = []
        self.pointer = 0
        self.relative_base = 0
        self.status = self.NOT_STARTED

    def output(self, clear_output=False):
        output = self.output_values
        if clear_output:
            self.output_values = []
        return output

    def ascii_output(self, clear_output=False):
        ascii_ouput = ""
        for c in self.output(clear_output):
            ascii_ouput += str(c)
        return ascii_ouput

    def last_output(self):
        return self.output_values[-1]

    def is_terminated(self):
        return self.status == self.TERMINATED

    def is_awaiting_input(self):
        return self.status == self.AWAITING_INPUT

    def add_inputs(self, input_values):
        self.input_values += input_values

    def run_program(self, input_values=[]):
        self.add_inputs(input_values)
        self.status = self.RUNNING
        while self.status == self.RUNNING:
            opcode, param_modes = self.next_operation()
            self.functions[opcode](self, param_modes)
        return self.last_output()

    def write_to_memory(self, value, location):
        self.memory[location] = value

    def read_memory(self, location):
        return self.memory.get(location, 0)

    def read_memory_and_advance(self):
        value = self.read_memory(self.pointer)
        self.pointer += 1
        return value

    def next_operation(self):
        opcode = self.read_memory_and_advance()
        opcode_str = f"{opcode:05}"
        opcode = int(opcode_str[3:5])
        param_modes = (int(opcode_str[2]), int(opcode_str[1]), int(opcode_str[0]))
        logging.debug(f"\nOperation: #{opcode_str}")
        return opcode, param_modes

    def read_parameter(self, param_mode, indirect=True):
        param = self.read_memory_and_advance()
        if param_mode == 1:
            logging.debug(f"Immediate parameter: {param}")
            return param
        if param_mode == 2:
            logging.debug(
                f"Add relative_base to parameter: {param} + {self.relative_base}"
            )
            param += self.relative_base
        if indirect:
            logging.debug(
                f"Reading parameter from location[{param}] ==> {self.read_memory(param)}"
            )
            param = self.read_memory(param)
        return param

    def terminate(self, *args, **kwargs):
        self.status = self.TERMINATED

    def add(self, param_modes, *args, **kwargs):
        a = self.read_parameter(param_modes[0])
        b = self.read_parameter(param_modes[1])
        location = self.read_parameter(param_modes[2], indirect=False)
        logging.debug(f"Adding {a} and {b} and storing at location: {location}")
        self.write_to_memory(a + b, location)

    def multiply(self, param_modes, *args, **kwargs):
        a = self.read_parameter(param_modes[0])
        b = self.read_parameter(param_modes[1])
        location = self.read_parameter(param_modes[2], indirect=False)
        logging.debug(f"Multiplying {a} and {b} and storing at location: {location}")
        self.write_to_memory(a * b, location)

    def take_input(self, param_modes, *args, **kwargs):
        location = self.read_parameter(param_modes[0], indirect=False)
        try:
            value = self.input_values.pop(0)
            logging.debug(f"Storing input ({value}) at location: {location}")
            self.write_to_memory(value, location)
        except IndexError:
            logging.debug(f"Awaiting input...")
            self.pointer -= 2
            self.status = self.AWAITING_INPUT

    def show_output(self, param_modes, *args, **kwargs):
        output = self.read_parameter(param_modes[0])
        logging.debug(f"Outputing value: {output}")
        self.output_values.append(output)

    def jump_if_true(self, param_modes, *args, **kwargs):
        value = self.read_parameter(param_modes[0])
        location = self.read_parameter(param_modes[1])
        logging.debug(f"If {value} is not zero: jump to {location}")
        if value:
            self.pointer = location

    def jump_if_false(self, param_modes, *args, **kwargs):
        value = self.read_parameter(param_modes[0])
        location = self.read_parameter(param_modes[1])
        logging.debug(f"If {value} is zero: jump to {location}")
        if not value:
            self.pointer = location

    def less_than(self, param_modes, *args, **kwargs):
        a = self.read_parameter(param_modes[0])
        b = self.read_parameter(param_modes[1])
        location = self.read_parameter(param_modes[2], indirect=False)
        logging.debug(f"Testing if {a} less than {b} => {location}")
        self.write_to_memory(int(a < b), location)

    def equals(self, param_modes, *args, **kwargs):
        a = self.read_parameter(param_modes[0])
        b = self.read_parameter(param_modes[1])
        location = self.read_parameter(param_modes[2], indirect=False)
        logging.debug(f"Testing if {a} equals {b} => {location}")
        self.write_to_memory(int(a == b), location)

    def adjust_relative_base(self, param_modes, *args, **kwargs):
        offset = self.read_parameter(param_modes[0])
        self.relative_base += offset
        logging.debug(f"Adjusting relative base by {offset} => {self.relative_base}")

    functions = {
        1: add,
        2: multiply,
        3: take_input,
        4: show_output,
        5: jump_if_true,
        6: jump_if_false,
        7: less_than,
        8: equals,
        9: adjust_relative_base,
        99: terminate,
    }


class IntCodeComputerNetwork:
    def __init__(self, program, number_of_computers=1):
        self.number_of_computers = number_of_computers
        self.computers = [IntCodeComputer(program) for _ in range(number_of_computers)]

    def add_inputs(self, inputs):
        for k, v in inputs.items():
            self.computers[k].add_inputs(v)

    def run_program(self, input_value):
        next_input = input_value
        i = 0
        while not self.computers[-1].is_terminated():
            logging.debug(f"Running computer {i+1} with input: {next_input}")
            next_input = self.computers[i].run_program([next_input])
            i = (i + 1) % self.number_of_computers
        return self.computers[-1].last_output()
