from pathlib import Path
from math import inf

def parse_wires(raw_data):
    wires = list()
    for raw_wire in raw_data.split():
        wire = set()
        curr_point = 0, 0
        for turn in raw_wire.split(","):
            direction, distance = turn[0], turn[1:]
            for d in range(int(distance)):
                if direction == "R":
                    next_point = curr_point[0] + 1, curr_point[1]

                elif direction == "L":
                    next_point = curr_point[0] - 1, curr_point[1]

                elif direction == "U":
                    next_point = curr_point[0], curr_point[1] + 1

                elif direction == "D":
                    next_point = curr_point[0], curr_point[1] - 1

                wire.add(next_point)
                curr_point = next_point

        wires.append(wire)

    return wires

def solve(wires):
    wire1, wire2 = wires
    cross_points = wire1.intersection(wire2)
    closest = inf
    for cross_point in cross_points:
        cross_x, cross_y = cross_point
        distance = abs(cross_x) + abs(cross_y)
        closest = min(distance, closest)

    return closest

if __name__ == "__main__":
    raw_data = Path("aoc3.txt").read_text()
    dist1 = solve(parse_wires(raw_data))
    print("Part 1:", dist1)
