from pathlib import Path

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

def simulate_step(moons, velocities=None):
    if velocities is None:
        velocities = [{"x": 0, "y": 0, "z": 0} for i in range(len(moons))]
    
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

if __name__ == "__main__":
    #moons = parse_moons("\n".join([
    #    "<x=-1, y=0, z=2>",
    #    "<x=2, y=-10, z=-7>",
    #    "<x=4, y=-8, z=8>",
    #    "<x=3, y=5, z=-1>",
    #]))
    moons = parse_moons(Path("aoc12.txt").read_text())
    velocities = None
    for i in range(1000):
        moons, velocities = simulate_step(moons, velocities)

    energy = compute_energy(moons, velocities)
    print("Part 1:", energy)
