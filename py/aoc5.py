from pathlib import Path
from copy import deepcopy

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

    def run(self, debug=False, quiet=False):
        state = self.parse()
        position = 0
        outputs = list()
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
                self.set_value(state, position, 1, int(input("> ")))
                position = position + 2

            elif opcode == 4:
                input1 = self.get_value(state, position, 1, modes)
                if not quiet:
                    print(f"-> {input1}")

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

        if debug:
            return state

        return outputs

if __name__ == "__main__":
    ic = IntCode(Path("../etc/aoc5.txt").read_text())

    result1 = ic.run(quiet=True)
    print("Part 1", result1[-1])

    result2 = ic.run(quiet=True)
    print("Part 2", result2[-1])
