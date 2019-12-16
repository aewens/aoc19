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

def render(px, py, walls):
    # Clears screen
    print(chr(27) + "[2J")

    min_x, min_y = px, px 
    max_x, max_y = px, py

    for wall in walls.keys():
        wx, wy = wall
        min_x = min(wx, min_x)
        min_y = min(wy, min_y)
        max_x = max(wx, max_x)
        max_y = max(wy, max_y)

    for y in range(min_y, max_y + 1):
        row = list()
        for x in range(min_x, max_x + 1):
            if x == px and y == py:
                row.append("@")
                continue

            wall = walls.get((x, y))
            row.append("#" if wall else " ")

        print("".join(row))

def _droid(ic, display=True):
    #moves = [1, 2, 3, 4]
    walls = defaultdict(lambda: False)
    known = defaultdict(dict)
    route = list()
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
    move = 1
    mode = "discover:check"
    checked = 1
    checking = px, py
    input_codes = [move]

    while status != 2:
        exit_code, meta = ic.run(input_codes[:], meta, quiet=True)
        if exit_code > 0:
            print("ERROR!")
            break

        here = known[checking]
        nx, ny = step[move](px, py)
        status = meta["outputs"][0]
        #print((px, py), input_codes, status, mode, here)
        #sleep(1) 
        if display:
            render(px, py, walls)
            print(mode, status, move, here)
            sleep(1)#0.1)

        if status == 2:
            print(nx, ny, walls)
            break

        if status == 0:
            walls[(nx, ny)] = True
            if mode == "discover:check" and len(here) < 4:
                here[move] = False
                checked = move
                move = (checked % 4) + 1

            elif mode == "discover:undo":
                print("LOGIC ERROR!")
                break

            if mode.startswith("discover") and len(here) == 4:
                options = [option for option, can in here.items() if can]
                if len(options) == 0:
                    mode = "back"

                else:
                    mode = "discover:check"
                    route.append(checking)
                    move = options[0]
                    steps.append(move)
                    px, py = step[move](px, py)
                    checking = px, py

        elif status == 1:
            if mode == "discover:check" and len(here) < 4:
                here[move] = True
                checked = move
                mode = "discover:undo"
                move = back[move]

            elif mode == "discover:undo" and len(here) < 4:
                mode = "discover:check"
                move = (checked % 4) + 1
                px, py = step[move](nx, ny)

            elif mode.startswith("discover") and len(here) == 4:
                options = [option for option, can in here.items() if can]
                if len(options) == 0:
                    mode = "back"

                else:
                    mode = "discover:check"
                    route.append(checking)
                    move = options[0]
                    steps.append(move)
                    px, py = step[move](px, py)
                    checking = px, py

        if mode != "back":
            input_codes = [move]

        else:
            input_codes = list()
            while True:
                prev_xy = route.pop()
                prev_step = steps.pop()

                previous = known[prev_xy]
                dead_end, *options = [o for o, c in previous.items() if c]
                previous[dead_end] = False
                if len(options) == 0:
                    input_codes.append(back[prev_step])
                    continue

                mode == "discover:check"
                px, py = prev_xy
                move = options[0]
                steps.append(move)
                px, py = step[move](px, py)
                input_codes.append(move)
                break

def droid(ic, display=True):
    walls = defaultdict(lambda: False)
    skip = defaultdict(set)
    route = list()
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
    move = 1
    checking = px, py
    input_codes = [move]

    while status != 2:
        exit_code, meta = ic.run(input_codes[:], meta, quiet=True)
        if exit_code > 0:
            print("ERROR!")
            break

        skipping = skip[(px, py)]
        nx, ny = step[move](px, py)
        status = meta["outputs"][0]
        if display:
            render(px, py, walls)
            print(status, move, (px, py), skipping)
            sleep(0.1)

        if status == 2:
            print(nx, ny, walls)

        elif status == 0:
            skipping.add(move)
            walls[(nx, ny)] = True

        elif status == 1:
            route.append((px, py))
            px, py = nx, ny

        backtrack = True
        if move in skipping:
            move = (move % 4) + 1
            for i in range(4):
                move = (move % 4) + 1
                if move in skipping:
                    continue

                test = step[move](px, py)
                if test not in route:
                    backtrack = False
                    break

        else:
            backtrack = False

        if backtrack:
            prev_xy = route.pop()
            prev_step = steps.pop()
            #print(px, py, prev_xy)
            #print(skip)

            skipping.add(prev_step)
            skipping = skip[prev_xy]
            skipping.add(prev_step)

            move = back[prev_step]

        steps.append(move)
        input_codes = [move]

if __name__ == "__main__":
    ic = IntCode(Path("aoc15.txt").read_text())
    droid(ic)
