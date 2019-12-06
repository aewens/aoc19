from collections import defaultdict
from pathlib import Path

def parse_map(text_map):
    orbits = text_map.split()
    orbit_map = defaultdict(set)
    for orbit in orbits:
        parent, child = orbit.split(")")
        orbit_map[parent].add(child)

    return orbit_map

def count_orbits(orbit_map, check=None, chain=list(), count=(0, 0)):
    if check is None:
        check = orbit_map.get("COM")
        if check is None:
            return count

    for orbit in check:
        direct, indirect = count
        direct = direct + 1
        indirect = indirect + len(chain)
        new_count = direct, indirect

        new_check = orbit_map.get(orbit)
        if new_check is not None:
            new_chain = chain + [orbit]
            count = count_orbits(orbit_map, new_check, new_chain, new_count)

        else:
            count = new_count

    return count

if __name__ == "__main__":
    orbit_map = parse_map(Path("aoc6.txt").read_text())
    total_orbits = sum(count_orbits(orbit_map))
    print("Part 1:", total_orbits)
