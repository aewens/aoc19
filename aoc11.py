from pathlib import Path
from copy import deepcopy
from itertools import permutations
from collections import defaultdict

class IntCode:
    def __init__(self, program):
        self.program = program

    def parse(self):
        memory = defaultdict(lambda: 0)
        init = list(map(int, deepcopy(self.program).strip().split(",")))
        for index, value in enumerate(init):
            memory[index] = value

        return memory

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

        elif mode == 1:
            value_position = position + offset

        elif mode == 2:
            rel_base = meta["rel_base"]
            rel_offset = state[position + offset]
            value_position = rel_base + rel_offset

        else:
            print(f"ERROR: modes={mode}, {modes}")
            return None

        if value_position < 0:
            print("ERROR:", value_position)

        value = state[value_position]
        return value

    def set_value(self, meta, offset, value):
        state = meta["state"]
        position = meta["position"]

        modes = meta["modes"]
        mode = self.get_mode(modes, offset)
        if mode == 0:
            result_position = state[position + offset]

        elif mode == 2:
            rel_base = meta["rel_base"]
            rel_offset = state[position + offset]
            result_position = rel_base + rel_offset

        else:
            print(f"ERROR: modes={mode}, {modes}")

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
            meta["rel_base"] = 0

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

            elif opcode == 9:
                input1 = self.get_value(meta, 1)
                rel_base = meta["rel_base"]
                meta["rel_base"] = rel_base + input1
                self.move_position(meta, 2)

            elif opcode == 99:
                break

            else:
                print(f"ERROR: {position}, {opcode}")
                return 1, meta

        return 0, meta

def robot(ic, quiet=False):
    meta = None
    input_codes = [0]
    facing = 0
    position = 0, 0
    panels = defaultdict(lambda: 0)
    painted = set()
    while True:
        exit_code, meta = ic.run([panels[position]], meta, quiet=quiet)
        if exit_code == 0:
            break

        elif exit_code > 0:
            print("ERROR!!!")
            break

        color, direction = meta["outputs"]
        panels[position] = color
        painted.add(position)
        if direction == 0:
            facing = (facing - 1) % 4
        elif direction == 1:
            facing = (facing + 1) % 4

        px, py = position
        if facing == 0:
            position = px, py - 1

        elif facing == 1:
            position = px + 1, py

        elif facing == 2:
            position = px, py + 1

        elif facing == 3:
            position = px - 1, py

    return painted

if __name__ == "__main__":
    ic = IntCode(Path("aoc11.txt").read_text())
    painted = robot(ic, True)

    print("Part 1:", len(painted))
