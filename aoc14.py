from pathlib import Path
from math import ceil
from sys import maxsize
from pprint import pprint

def parse_reactions(raw_text):
    reactions = dict()
    r_inputs = reactions["inputs"] = list()
    r_outputs = reactions["outputs"] = list()
    for line in raw_text.split("\n"):
        if len(line) == 0:
            continue

        inputs, output = line.strip().split(" => ")
        output_value, output_key = output.split(" ")
        r_outputs.append({output_key: int(output_value)})
        pairs = dict()
        for pair in inputs.split(", "):
            value, key = pair.split(" ")
            pairs[key] = int(value)

        r_inputs.append(pairs)

    return reactions

def get_chemical_quantity(reactions, chemical, fuel=1):
    inputs = reactions.get("inputs")
    outputs = reactions.get("outputs")

    if chemical == "FUEL":
        return fuel

    quantity = 0
    for p, pairs in enumerate(inputs):
        if chemical in pairs:
            output = outputs[p]
            for output_chemical, output_quantity in output.items():
                args = reactions, output_chemical, fuel
                chemical_quantity = get_chemical_quantity(*args)
                current_quantity = pairs.get(chemical)
                used_quantity = ceil(chemical_quantity / output_quantity)
                quantity = quantity + used_quantity * current_quantity

    return quantity

def get_fuel_units(reactions):
    min_fuel = 1
    max_fuel = maxsize - 1
    available_ore = 10**12
    while (max_fuel - min_fuel) > 1:
        make = (min_fuel + max_fuel) // 2
        ores = get_chemical_quantity(reactions, "ORE", make)
        if ores <= available_ore:
            min_fuel = make

        else:
            max_fuel = make

    return min_fuel

if __name__ == "__main__":
    #reactions = parse_reactions("\n".join([
    #    "157 ORE => 5 NZVS",
    #    "165 ORE => 6 DCFZ",
    #    "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
    #    "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ","179 ORE => 7 PSHF",
    #    "177 ORE => 5 HKGWZ",
    #    "7 DCFZ, 7 PSHF => 2 XJWVT",
    #    "165 ORE => 2 GPVTF",
    #    "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"
    #]))
    reactions = parse_reactions(Path("aoc14.txt").read_text())
    count = get_chemical_quantity(reactions, "ORE")
    print("Part 1:", count)
    fuel = get_fuel_units(reactions)
    print("Part 2:", fuel)
