from pathlib import Path
from copy import deepcopy
from itertools import permutations
from collections import defaultdict
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

def get_tiles(meta, tiles):
    data = meta.get("outputs", list())

    cursor = 0
    tile_types = dict()
    tile_types[0] = "empty"
    tile_types[1] = "wall"
    tile_types[2] = "block"
    tile_types[3] = "paddle"
    tile_types[4] = "ball"
    while cursor < len(data):
        tile_x = data[cursor + 0]
        tile_y = data[cursor + 1]
        if tile_x == -1 and tile_y == 0:
            score = data[cursor + 2]
            tiles["score"] = score
            cursor = cursor + 3
            continue
        
        tile_id = data[cursor + 2]
        tile_type = tile_types.get(tile_id, "invalid")
        tiles[(tile_x, tile_y)] = tile_type
        cursor = cursor + 3

    return tiles

def get_blocks(tiles):
    blocks = 0
    for position, tile_type in tiles.items():
        if tile_type == "block":
            blocks = blocks + 1

    return blocks

def display_tiles(tiles):
    score = tiles.get("score", 0)
    render = dict()
    render["empty"] = " " 
    render["wall"] = "*"
    render["block"] = "#"
    render["paddle"] = "="
    render["ball"] = "@"
    max_x, max_y = list(tiles.keys())[-2]
    for y in range(max_y + 1):
        line = list()
        for x in range(max_x + 1):
            tile = tiles.get((x, y), "invalid")
            if tile == "invalid":
                print(tiles)
                print(x, y)
                return
            line.append(render.get(tile, "x"))

        print("".join(line))

    print("Score: ", score)

def get_input(tiles):
    paddle = None
    ball = None
    for position, tile_type in tiles.items():
        if tile_type == "paddle":
            paddle = position

        elif tile_type == "ball":
            ball = position

        if None not in [paddle, ball]:
            break

    px = paddle[0]
    bx = ball[0]

    if px > bx:
        return -1

    elif px == bx:
        return 0

    elif px < bx:
        return 1

def arcade(ic, display=True, auto=True):
    # Insert quarters
    meta = ic.dump()
    meta["state"][0] = 2

    exit_code = None
    tiles = dict()
    joystick = list()
    joystick_map = dict()
    joystick_map["j"] = -1
    joystick_map["k"] = 0
    joystick_map["l"] = 1
    while exit_code != 0:
        exit_code, meta = ic.run(joystick, meta, quiet=True)
        tiles = get_tiles(meta, tiles)
        if exit_code == 0:
            print("Part 2:", tiles.get("score", 0))

        elif exit_code > 0:
            print("ERROR!")
            break

        else:
            if display:
                display_tiles(tiles)
                if auto:
                    sleep(0.1)

            if auto:
                joystick = [get_input(tiles)]

            else:
                joystick = [joystick_map.get(input("[j,k,l]> "), 0)]

if __name__ == "__main__":
    ic = IntCode(Path("aoc13.txt").read_text())
    exit_code, meta = ic.run([], quiet=True)
    if exit_code != 0:
        print("ERROR!")

    blocks = get_blocks(get_tiles(meta, dict()))
    print("Part 1:", blocks)

    arcade(ic, False)
