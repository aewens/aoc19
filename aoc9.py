from pathlib import Path
from copy import deepcopy
from itertools import permutations

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

    def get_value(self, meta, offset):
        state = meta["state"]
        position = meta["position"]
        modes = meta["modes"]
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

    def set_value(self, meta, offset, value):
        state = meta["state"]
        position = meta["position"]
        #modes = meta["modes"]
        #mode = self.get_mode(modes, offset)
        result_position = state[position + offset]
        state[result_position] = value
        meta.update({"state": state})

    def next_step(self, meta):
        state = meta["state"]
        position = meta["position"]
        settings = str(state[position])

        modes = settings[:-2][::-1]
        meta.update({"modes": modes})

        opcode = int(settings[-2:])
        return opcode

    def move_position(self, meta, value, override=False):
        position = value if override else meta["position"] + value
        meta.update({"position": position})

    def run(self, input_codes, meta=None, quiet=False):
        if meta is None:
            meta = dict()
            meta["state"] = self.parse()
            meta["position"] = 0
            
        meta["outputs"] = list()

        while True:
            opcode = self.next_step(meta)

            if opcode == 1:
                input1 = self.get_value(meta, 1)
                input2 = self.get_value(meta, 2)
                self.set_value(meta, 3, input1 + input2)
                self.move_position(meta, 4)

            elif opcode == 2:
                input1 = self.get_value(meta, 1)
                input2 = self.get_value(meta, 2)
                self.set_value(meta, 3, input1 * input2)
                self.move_position(meta, 4)

            elif opcode == 3:
                if len(input_codes) == 0:
                    return -1, meta

                input_code = input_codes.pop(0)
                if not quiet:
                    print(f"<- {input_code}")

                self.set_value(meta, 1, input_code)
                self.move_position(meta, 2)

            elif opcode == 4:
                input1 = self.get_value(meta, 1)
                if not quiet:
                    print(f"-> {input1}")

                meta["outputs"].append(input1)
                self.move_position(meta, 2)

            elif opcode == 5:
                input1 = self.get_value(meta, 1)
                input2 = self.get_value(meta, 2)
                if input1 != 0:
                    self.move_position(meta, input2, True)

                else:
                    self.move_position(meta, 3)

            elif opcode == 6:
                input1 = self.get_value(meta, 1)
                input2 = self.get_value(meta, 2)
                if input1 == 0:
                    self.move_position(meta, input2, True)

                else:
                    self.move_position(meta, 3)

            elif opcode == 7:
                input1 = self.get_value(meta, 1)
                input2 = self.get_value(meta, 2)
                self.set_value(meta, 3, 1 if input1 < input2 else 0)
                self.move_position(meta, 4)

            elif opcode == 8:
                input1 = self.get_value(meta, 1)
                input2 = self.get_value(meta, 2)
                self.set_value(meta, 3, 1 if input1 == input2 else 0)
                self.move_position(meta, 4)

            elif opcode == 99:
                break

            else:
                print(f"ERROR: {position}, {opcode}")
                return 1, meta

        return 0, meta

def solve(ic, seq_range, init_input_codes, stream=False, quiet=False):
    max_signal = -1
    max_sequence = None
    for sequence in permutations(seq_range, len(seq_range)):
        if stream:
            streams = [[phase_setting] for phase_setting in sequence]
            streams[0].append(init_input_codes[0])

            complete = [False for s in range(len(sequence))]
            metas = [None for s in range(len(sequence))]

            while not all(complete):
                for seq_index in range(len(sequence)):
                    next_index = (seq_index + 1) % len(streams)
                    meta = metas[seq_index]
                    reader = streams[seq_index]
                    writer = streams[next_index]
                    args = reader, meta, quiet
                    exit_code, new_meta = ic.run(reader, meta, quiet=quiet)
                    if exit_code > 0:
                        return None, None

                    metas[seq_index] = new_meta

                    outputs = new_meta["outputs"]
                    writer.extend(outputs)

                    if exit_code == 0:
                        complete[seq_index] = True

            signal = streams[0][-1]

        else:
            input_codes = init_input_codes
            for phase_setting in sequence:
                phase_input_codes = [phase_setting] + input_codes
                exit_code, meta = ic.run(phase_input_codes, quiet=quiet)
                input_codes = meta.get("outputs")

            signal = input_codes[0]

        if signal > max_signal:
            max_signal = signal
            max_sequence = sequence

    return max_signal, max_sequence

if __name__ == "__main__":
    ic = IntCode(Path("aoc9.txt").read_text())
