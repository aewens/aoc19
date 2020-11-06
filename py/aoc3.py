from pathlib import Path
from math import inf

def parse_wires(raw_data):
    steps = list()
    points = list()
    for raw_wire in raw_data.split():
        wire_steps = dict()
        wire_points = set()
        curr_point = 0, 0
        curr_steps = 0
        for turn in raw_wire.split(","):
            direction, distance = turn[0], int(turn[1:])
            for d in range(distance):
                if direction == "R":
                    next_point = curr_point[0] + 1, curr_point[1]

                elif direction == "L":
                    next_point = curr_point[0] - 1, curr_point[1]

                elif direction == "U":
                    next_point = curr_point[0], curr_point[1] + 1

                elif direction == "D":
                    next_point = curr_point[0], curr_point[1] - 1

                curr_steps = curr_steps + 1
                step_key = ":".join(map(str, next_point))
                wire_step = wire_steps.get(step_key)
                if not wire_step:
                    wire_steps[step_key] = curr_steps

                wire_points.add(next_point)
                curr_point = next_point

        steps.append(wire_steps)
        points.append(wire_points)

    return points, steps

def get_crosses(wires):
    wire1, wire2 = wires
    cross_points = wire1.intersection(wire2)
    return cross_points

def closest_cross(cross_points):
    closest = inf
    for cross_point in cross_points:
        cross_x, cross_y = cross_point
        distance = abs(cross_x) + abs(cross_y)
        closest = min(distance, closest)

    return closest

def fewest_steps(cross_points, wire_steps):
    steps1, steps2 = wire_steps
    fewest = inf
    for cross_point in cross_points:
        step_key = ":".join(map(str, cross_point))
        step1 = steps1[step_key]
        step2 = steps2[step_key]
        steps = step1 + step2
        fewest = min(steps, fewest)

    return fewest

if __name__ == "__main__":
    raw_data = Path("../etc/aoc3.txt").read_text()
    wire_points, wire_steps = parse_wires(raw_data)
    cross_points = get_crosses(wire_points)
    closest = closest_cross(cross_points)
    print("Part 1:", closest)
    fewest = fewest_steps(cross_points, wire_steps)
    print("Part 2:", fewest)
