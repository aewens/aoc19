from pathlib import Path
from copy import deepcopy
from collections import defaultdict
from operator import itemgetter
from math import inf
from time import sleep

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

    def dump(self):
        meta = dict()
        meta["state"] = self.parse()
        meta["position"] = 0
        meta["rel_base"] = 0

        return meta

    def run(self, input_codes, meta=None, quiet=False):
        if meta is None:
            meta = self.dump()

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

def render(px, py, ship):
    # Clears screen
    print(chr(27) + "[2J")

    min_x, min_y = px - 1, px - 1
    max_x, max_y = px + 1, py + 1

    for sxy in ship.keys():
        sx, sy = sxy
        min_x = min(sx, min_x)
        min_y = min(sy, min_y)
        max_x = max(sx, max_x)
        max_y = max(sy, max_y)

    for y in range(min_y, max_y + 1):
        row = list()
        for x in range(min_x, max_x + 1):
            if x == px and y == py:
                row.append("@")
                continue

            status = ship.get((x, y))
            if status == -1 or status is None:
                row.append("#")

            elif status == 0:
                row.append("%")

            elif status == 1:
                row.append(".")

            elif status == 2:
                row.append("&")

            else:
                row.append("*")

        print("".join(row))

def droid(ic, display=True):
    options = defaultdict(lambda: [1, 2, 3, 4])
    ship = defaultdict(lambda: -1)
    steps = list()

    step = dict()
    step[1] = lambda x, y: (x, y - 1)
    step[2] = lambda x, y: (x, y + 1)
    step[3] = lambda x, y: (x - 1, y)
    step[4] = lambda x, y: (x + 1, y)

    back = dict()
    back[1] = 2
    back[2] = 1
    back[3] = 4
    back[4] = 3

    meta = ic.dump()

    px, py = 0, 0
    status = -1
    move = options[(px, py)].pop()

    while status != 2:
        moves = options[(px, py)]
        if len(moves) > 0:
            backtrack = False
            move = moves.pop()

        else:
            backtrack = True
            previous = steps.pop()
            move = back[previous]

        exit_code, meta = ic.run([move], meta, quiet=True)
        if exit_code > 0:
            print("ERROR!")
            break

        nx, ny = step[move](px, py)
        status = meta["outputs"][0]

        if display:
            render(px, py, ship)
            print(status, move, (px, py))
            sleep(0.05)

        if status == 2:
            print(nx, ny)
            break

        elif status == 1:
            px, py = nx, ny
            ship[(px, py)] = status
            if not backtrack:
                steps.append(move)

if __name__ == "__main__":
    ic = IntCode(Path("aoc15.txt").read_text())
    droid(ic)
