from pathlib import Path

class IntCode:
    def __init__(self, program):
        self.program = program

    def parse(self):
        return list(map(int, self.program.strip().split(",")))

    def run(self, alarm=False):
        state = self.parse()
        if alarm:
            state[1] = 12
            state[2] = 2

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

if __name__ == "__main__":
    ic = IntCode(Path("aoc2.txt").read_text())
    result = ic.run(True)
    print("Part 1:", result[0])
