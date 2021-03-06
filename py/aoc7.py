from pathlib import Path
from copy import deepcopy
from itertools import permutations
from threading import Thread
from queue import Queue

class IntCode:
    def __init__(self, program):
        self.program = program

    def parse(self):
        return list(map(int, deepcopy(self.program).strip().split(",")))

    def pad(self, value, length):
        diff = (length + 1)- len(value)
        return value + ("0" * diff)

    def get_mode(self, modes, offset):
        mode_offset = offset - 1
        if mode_offset >= len(modes):
            modes = self.pad(modes, mode_offset)

        return int(modes[mode_offset])

    def get_value(self, state, position, offset, modes):
        mode = self.get_mode(modes, offset)
        value = None
        if mode == 0:
            value_position = state[position + offset]
            try:
                value = state[value_position]

            except Exception as e:
                print(f"ERROR position[0]={position + offset}, {len(state)}")

        elif mode == 1:
            try:
                value = state[position + offset]

            except Exception as e:
                print(f"ERROR position[1]={position + offset}, {len(state)}")

        else:
            print(f"ERROR: modes={mode}, {modes}")

        return value

    def set_value(self, state, position, offset, value):
        result_position = state[position + offset]
        state[result_position] = value

    def run(self, input_codes, quiet=False, stream=None):
        state = self.parse()
        position = 0
        outputs = list()
        if stream:
            reader, writer = stream

        while True:
            settings = str(state[position])
            modes, opcode = settings[:-2][::-1], int(settings[-2:])

            if opcode == 1:
                input1 = self.get_value(state, position, 1, modes)
                input2 = self.get_value(state, position, 2, modes)
                self.set_value(state, position, 3, input1 + input2)
                position = position + 4

            elif opcode == 2:
                input1 = self.get_value(state, position, 1, modes)
                input2 = self.get_value(state, position, 2, modes)
                self.set_value(state, position, 3, input1 * input2)
                position = position + 4

            elif opcode == 3:
                input_code = reader.get() if stream else input_codes.pop(0)
                self.set_value(state, position, 1, input_code)
                position = position + 2

            elif opcode == 4:
                input1 = self.get_value(state, position, 1, modes)
                if not quiet:
                    print(f"-> {input1}")

                if stream:
                    writer.put(input1)

                outputs.append(input1)
                position = position + 2

            elif opcode == 5:
                input1 = self.get_value(state, position, 1, modes)
                input2 = self.get_value(state, position, 2, modes)
                if input1 != 0:
                    position = input2

                else:
                    position = position + 3

            elif opcode == 6:
                input1 = self.get_value(state, position, 1, modes)
                input2 = self.get_value(state, position, 2, modes)
                if input1 == 0:
                    position = input2

                else:
                    position = position + 3

            elif opcode == 7:
                input1 = self.get_value(state, position, 1, modes)
                input2 = self.get_value(state, position, 2, modes)
                self.set_value(state, position, 3, 1 if input1 < input2 else 0)
                position = position + 4

            elif opcode == 8:
                input1 = self.get_value(state, position, 1, modes)
                input2 = self.get_value(state, position, 2, modes)
                self.set_value(state, position, 3, 1 if input1 == input2 else 0)
                position = position + 4

            elif opcode == 99:
                break

            else:
                print(f"ERROR: {position}, {opcode}")
                break

        if stream:
            writer.put(outputs[-1])

        return outputs

    def solve(self, seq_range, init_input_codes, quiet=False, stream=False):
        max_signal = -1
        max_sequence = None
        for sequence in permutations(seq_range, len(seq_range)):
            if stream:
                procs = list()
                streams = [Queue() for i in range(len(sequence))]
                for s, phase_setting in enumerate(sequence):
                    reader = streams[s]
                    writer = streams[(s + 1) % len(streams)]
                    reader.put(phase_setting)
                    args = list(), quiet, (reader, writer)
                    proc = Thread(target=self.run, args=args)
                    procs.append(proc)
                    proc.start()

                streams[0].put(init_input_codes[0])
                for proc in procs:
                    proc.join()

                signal = streams[0].get()

            else:
                input_codes = init_input_codes
                for phase_setting in sequence:
                    phase_input_codes = [phase_setting] + input_codes
                    input_codes = self.run(phase_input_codes, quiet=quiet)

                signal = input_codes[0]

            if signal > max_signal:
                max_signal = signal
                max_sequence = sequence

        return max_signal, max_sequence

if __name__ == "__main__":
    ic = IntCode(Path("../etc/aoc7.txt").read_text())

    result1 = ic.solve(list(range(5)), [0], quiet=True)
    print("Part 1:", result1[0])

    result2 = ic.solve(list(range(5, 10)), [0], quiet=True, stream=True)
    print("Part 2:", result2[0])
