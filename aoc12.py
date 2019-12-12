from pathlib import Path
from copy import deepcopy

def parse_moons(raw_moons):
    moons = list()
    for line in raw_moons.strip().split("\n"):
        moon = dict()
        positions = line.strip()[1:-1].split(",")
        for position in positions:
            key, value = position.strip().split("=")
            moon[key] = int(value)

        moons.append(moon)

    return moons

def simulate_step(moons, velocities):
    for m, moon in enumerate(moons):
        mx = moon["x"]
        my = moon["y"]
        mz = moon["z"]
        
        velocity = velocities[m]
        gx = velocity["x"]
        gy = velocity["y"]
        gz = velocity["z"]
        for mm, mmoon in enumerate(moons):
            if m == mm:
                continue

            mmx = mmoon["x"]
            mmy = mmoon["y"]
            mmz = mmoon["z"]

            if mx != mmx:
                dx = 1 if mx < mmx else -1
                gx = gx + dx

            if my != mmy:
                dy = 1 if my < mmy else -1
                gy = gy + dy

            if mz != mmz:
                dz = 1 if mz < mmz else -1
                gz = gz + dz

        velocities[m] = {"x": gx, "y": gy, "z": gz}

    for v, velocity in enumerate(velocities):
        moon = moons[v]
        mx = moon["x"]
        my = moon["y"]
        mz = moon["z"]

        vx = velocity["x"]
        vy = velocity["y"]
        vz = velocity["z"]

        moon["x"] = mx + vx
        moon["y"] = my + vy
        moon["z"] = mz + vz

    return moons, velocities

def compute_energy(moons, velocities):
    energy = 0
    for m, moon in enumerate(moons):
        velocity = velocities[m]
        potential = sum([abs(pos) for pos in moon.values()])
        kinetic = sum([abs(vel) for vel in velocity.values()])
        energy = energy + (potential * kinetic)

    return energy

def gcd(a, b):
    while b:
        a, b = b, a % b

    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def simulate_axis_step(positions, velocities):
    for p, pos in enumerate(positions):
        velocity = velocities[p]
        for pp, ppos in enumerate(positions):
            if p == pp:
                continue

            if pos != ppos:
                gravity = 1 if pos < ppos else -1
                velocity = velocity + gravity

        velocities[p] = velocity

    for v, velocity in enumerate(velocities):
        pos = positions[v]
        positions[v] = pos + velocity

    return positions, velocities

def find_first_repeat(moons, velocities):
    pos_x = list()
    vel_x = list()
    pos_y = list()
    vel_y = list()
    pos_z = list()
    vel_z = list()

    for m, moon in enumerate(moons):
        mx = moon["x"]
        my = moon["y"]
        mz = moon["z"]

        velocity = velocities[m]
        vx = velocity["x"]
        vy = velocity["y"]
        vz = velocity["z"]

        pos_x.append(mx)
        vel_x.append(vx)
        pos_y.append(my)
        vel_y.append(vy)
        pos_z.append(mz)
        vel_z.append(vz)

    ipx = deepcopy(pos_x)
    ivx = deepcopy(vel_x)
    ipy = deepcopy(pos_y)
    ivy = deepcopy(vel_y)
    ipz = deepcopy(pos_z)
    ivz = deepcopy(vel_z)

    steps_x, steps_y, steps_z = 0, 0, 0
    found_x, found_y, found_z = False, False, False
    while True:
        if all([found_x, found_y, found_z]):
            break

        if not found_x:
            pos_x, vel_x = simulate_axis_step(pos_x, vel_x)
            steps_x = steps_x + 1
            if pos_x == ipx and vel_x == ivx:
                found_x = True

        if not found_y:
            pos_y, vel_y = simulate_axis_step(pos_y, vel_y)
            steps_y = steps_y + 1
            if pos_y == ipy and vel_y == ivy:
                found_y = True

        if not found_z:
            pos_z, vel_z = simulate_axis_step(pos_z, vel_z)
            steps_z = steps_z + 1
            if pos_z == ipz and vel_z == ivz:
                found_z = True

    return lcm(lcm(steps_x, steps_y), steps_z)

if __name__ == "__main__":
    #moons = parse_moons("\n".join([
    #    "<x=-1, y=0, z=2>",
    #    "<x=2, y=-10, z=-7>",
    #    "<x=4, y=-8, z=8>",
    #    "<x=3, y=5, z=-1>",
    #]))
    #moons = parse_moons("\n".join([
    #    "<x=-8, y=-10, z=0>",
    #    "<x=5, y=5, z=10>",
    #    "<x=2, y=-7, z=3>",
    #    "<x=9, y=-8, z=-3>",
    #]))
    moons = parse_moons(Path("aoc12.txt").read_text())
    velocities = [{"x": 0, "y": 0, "z": 0} for i in range(len(moons))]
    init_moons = deepcopy(moons)
    init_velocities = deepcopy(velocities)
    for i in range(1000):
        moons, velocities = simulate_step(moons, velocities)

    energy = compute_energy(moons, velocities)
    print("Part 1:", energy)

    steps = find_first_repeat(init_moons, init_velocities)
    print("Part 2:", steps)

