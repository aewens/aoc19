#!/usr/bin/env python3

from math import floor
from pathlib import Path
from itertools import repeat

def fuel_required(mass, needed=False):
    init_fuel = floor(mass / 3) - 2
    if not needed:
        return init_fuel

    return fuel_required_for_fuel(init_fuel)

def fuel_required_for_fuel(fuel):
    total_fuel = fuel
    previous_fuel = fuel
    while True:
        needed_fuel = fuel_required(previous_fuel)
        if needed_fuel <= 0:
            break

        total_fuel = total_fuel + needed_fuel
        previous_fuel = needed_fuel

    return total_fuel

def load_modules(path):
    modules = list()
    if not path.exists():
        return modules

    raw_modules = path.read_text().split()
    for module in raw_modules:
        modules.append(int(module))

    return modules

if __name__ == "__main__":
    modules = load_modules(Path("aoc1.txt"))
    total_fuel = sum(map(fuel_required, modules))
    print(f"Part 1: {total_fuel}")

    total_fuel_needed = sum(map(fuel_required, modules, repeat(True)))
    print(f"Part 2: {total_fuel_needed}")
