from pathlib import Path
from copy import deepcopy

class IntCode:
    def __init__(self, program):
        self.program = program

    def parse(self):
        return list(map(int, deepcopy(self.program).strip().split(",")))

    def run(self, input_data):
        state = self.parse()
        state[1] = input_data[0]
        state[2] = input_data[1]

        position = 0
        while True:
            opcode = state[position]
            if opcode == 1:
                input1_position = state[position+1]
                input2_position = state[position+2]
                result_position = state[position+3]
                input1 = state[input1_position]
                input2 = state[input2_position]
                state[result_position] = input1 + input2
                position = position + 4

            elif opcode == 2:
                input1_position = state[position+1]
                input2_position = state[position+2]
                result_position = state[position+3]
                input1 = state[input1_position]
                input2 = state[input2_position]
                state[result_position] = input1 * input2
                position = position + 4

            elif opcode == 99:
                break

            else:
                print(f"ERROR: {position}, {opcode}")
                break

        return state

    def find(self, search):
        found = False
        noun = -1
        verb = -1
        for y in range(100):
            if found:
                break

            for x in range(100):
                result = self.run([x, y])
                if result[0] == search:
                    found = True
                    noun, verb = x, y
                    break

        return 100 * noun + verb

if __name__ == "__main__":
    ic = IntCode(Path("../etc/aoc2.txt").read_text())
    result1 = ic.run([12, 2])
    print("Part 1:", result1[0])

    result2 = ic.find(19690720)
    print("Part 2:", result2)
