#!/usr/bin/env python3

from math import floor
from pathlib import Path

def fuel_required(mass):
    return floor(mass / 3) - 2

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
    print(sum(map(fuel_required, modules)))
