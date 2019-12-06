from collections import defaultdict
from pathlib import Path

# DEBUG
from pprint import pprint

def parse_map(text_map):
    orbits = text_map.split()
    orbit_map = defaultdict(set)
    for orbit in orbits:
        parent, child = orbit.split(")")
        orbit_map[parent].add(child)

    return orbit_map

def count_orbits(orbit_map, graph=dict(), orbits=None, chain=list(), direct=0,
    indirect=0):
    if orbits is None:
        orbits = orbit_map.get("COM")
        if orbits is None:
            return direct, indirect

    for orbit in orbits:
        direct = direct + 1
        indirect = indirect + len(chain)

        satellites = orbit_map.get(orbit)
        if satellites is not None:
            chain_orbit = chain + [orbit]
            args = orbit_map, graph, satellites, chain_orbit, direct, indirect
            graph, direct, indirect = count_orbits(*args)

        else:
            graph[orbit] = ["COM"] + chain

    return graph, direct, indirect

def find_shortest_distance(graph):
    you = graph.get("YOU")
    san = graph.get("SAN")

    if None in [you, san]:
        return -1

    closest_intersection = None
    you_r = you[::-1]
    san_r = san[::-1]
    for orbit in you_r:
        if orbit in san_r:
            closest_intersection = orbit
            break

    you_i = you_r.index(closest_intersection)
    san_i = san.index(closest_intersection)
    path = you_r[1:you_i] + san[san_i:]

    return len(path)

if __name__ == "__main__":
    orbit_map = parse_map(Path("aoc6.txt").read_text())
    #orbit_map = parse_map("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN")
    graph, direct_orbits, indirect_orbits = count_orbits(orbit_map)
    total_orbits = direct_orbits + indirect_orbits
    print("Part 1:", total_orbits)

    distance = find_shortest_distance(graph)
    print("Part 2:", distance)
