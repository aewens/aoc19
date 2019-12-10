from pathlib import Path
from math import sqrt

def parse_map(raw_text):
    asteroids = list()
    for y, row in enumerate(raw_text.split()):
        for x, col in enumerate(list(row)):
            if col == "#":
                asteroids.append((x, y))

    return asteroids

# Distance between points a and b
def get_distance(a, b):
    ax, ay = a
    bx, by = b
    x2 = (ax - bx)**2
    y2 = (ay - by)**2
    return sqrt(x2 + y2)

# Determine if point b lies between a and c
def intersect2s(a, b, c):
    ab = get_distance(a, b)
    bc = get_distance(b, c)
    ac = get_distance(a, c)
    return (ab + bc) == ac

def dot(a, b):
    ax, ay = a
    bx, by = b
    abx = ax * bx
    aby = ay * by
    return abx + aby

def wedge(a, b):
    ax, ay = a
    bx, by = b
    axby = ax * by
    aybx = ay * bx
    return axby - aybx

def intersects(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c

    ux = ax - bx
    uy = ay - by
    u = ux, uy

    vx = bx - cx
    vy = by - cy
    v = vx, vy

    return wedge(u, v) == 0 and dot(u, v) > 0

def get_visible(points, check):
    visible = 0
    check_point = points[check]
    lines = [[check_point, point] for p, point in enumerate(points) if p != check]
    for line in lines:
        start, end = line
        blocked = False
        for p, point in enumerate(points):
            if p == check:
                continue

            if intersects(start, point, end):
                blocked = True
                break

        if not blocked:
            visible = visible + 1

    return visible

def get_most_visible(asteroid_map):
    most_visible = 0
    choice = None
    for asteroid in range(len(asteroid_map)):
        visible = get_visible(asteroid_map, asteroid)
        if visible > most_visible:
            most_visible = visible
            choice = asteroid_map[asteroid]

    return most_visible

if __name__ == "__main__":
    #asteroid_map = parse_map(test_case)
    asteroid_map = parse_map(Path("aoc10.txt").read_text())
    print("Part 1:", get_most_visible(asteroid_map))
