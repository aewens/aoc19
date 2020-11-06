from pathlib import Path
from math import atan2, hypot, pi
from operator import itemgetter
from collections import defaultdict

def parse_map(raw_text):
    asteroids = list()
    for y, row in enumerate(raw_text.split()):
        for x, col in enumerate(list(row)):
            if col == "#":
                asteroids.append((x, y))

    return asteroids

def angle_from(a, b):
    return atan2(b[0] - a[0], a[1] - b[1]) % (2 * pi)

def get_visible(asteroids, check):
    visible = set()
    for asteroid in asteroids:
        if asteroid == check:
            continue

        angle = angle_from(check, asteroid)
        visible.add(angle)

    return len(visible)

def get_most_visible(asteroid_map):
    most_visible = 0
    asteroids = None
    for asteroid in asteroid_map:
        visible = get_visible(asteroid_map, asteroid)
        most_visible = max(visible, most_visible)

    return most_visible

def dist_from(a, b):
    ax, ay = a
    bx, by = b

    return hypot(by - ay, bx - ax)

def destroy_order(blocks, station):
    return lambda asteroid: (blocks[asteroid], angle_from(station, asteroid))

def destroy_asteroids(asteroids):
    visibles = [(a, get_visible(asteroids, a)) for a in asteroids]
    visibles.sort(key=itemgetter(1))
    station = visibles[-1][0]
    asteroids.remove(station)

    asteroids.sort(key=lambda a: dist_from(station, a))
    blocks = defaultdict(lambda: 0)
    for a, asteroid in enumerate(asteroids):
        closest_asteroids = asteroids[:a]
        for close_asteroid in closest_asteroids:
            angle1 = angle_from(station, asteroid)
            angle2 = angle_from(station, close_asteroid)
            if angle1 == angle2:
                block = blocks[asteroid]
                blocks[asteroid] = block + 1

    order = destroy_order(blocks, station)
    return sorted(asteroids, key=lambda a: order(a))[200 - 1]

if __name__ == "__main__":
    asteroid_map = parse_map(Path("../etc/aoc10.txt").read_text())

    visible = get_most_visible(asteroid_map)
    print("Part 1:", visible)

    asteroid200 = destroy_asteroids(asteroid_map)
    x, y = asteroid200
    print("Part 2:", x * 100 + y)
