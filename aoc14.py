from pathlib import Path
from collections import defaultdict
from math import inf, ceil
from copy import deepcopy
from pprint import pprint

def parse_reactions(raw_text):
    reactions = dict()
    for line in raw_text.split("\n"):
        if len(line) == 0:
            continue

        raw_inputs, raw_output = line.strip().split(" => ")
        inputs = list()
        for r_input in raw_inputs.split(", "):
            quantity, chemical = r_input.split(" ")
            inputs.append((int(quantity), chemical))

        output_quantity, output_chemical = raw_output.split(" ")
        output = int(output_quantity), output_chemical
        reactions[output] = inputs

    return reactions

def get_refined_chemicals(reactions):
    refined = dict()
    chemicals = set()
    for reaction_output, reaction_inputs in reactions.items():
        if len(reaction_inputs) != 1:
            continue

        reaction_input = reaction_inputs[0]
        input_quantity, input_chemical = reaction_input
        if input_chemical != "ORE":
            continue

        output_quantity, output_chemical = reaction_output
        refined[reaction_output] = input_quantity
        chemicals.add(output_chemical)

    return chemicals, refined

def expand_reactions(reactions, refined):
    changed = True
    expanded_reactions = deepcopy(reactions)
    refined_chemicals, refined_reactions = refined
    expanded = True
    while expanded:
        expanded = False
        for reaction_output, reaction_inputs in expanded_reactions.items():
            output_quantity, output_chemical = reaction_output
            if output_chemical in refined_chemicals:
                continue

            expansions = list()
            for reaction_input in reaction_inputs:
                expansion = reactions.get(reaction_input)
                if expansion is None:
                    expansions.append(reaction_input)
                    continue

                expanded = True
                expansions.extend(expansion)

            expanded_reactions[reaction_output] = expansions

    return expanded_reactions

def expand_expansion_chemicals(n_chemicals, r_chemicals, outputs, reactions):
    for needed_chemical in list(n_chemicals.keys()):
        needed_quantity = n_chemicals[needed_chemical]
        if needed_chemical == "ORE" or needed_chemical in r_chemicals:
            n_chemicals[needed_chemical] = needed_quantity
            continue

        n_chemicals.pop(needed_chemical)
        available_quantity = outputs.get(needed_chemical)
        if needed_quantity < available_quantity:
            uses = 1

        else:
            uses = ceil(needed_quantity / available_quantity)

        reaction_inputs = reactions.get((available_quantity, needed_chemical))
        for input_quantity, input_chemical in reaction_inputs:
            current_quantity = n_chemicals[input_chemical]
            new_quantity = current_quantity + input_quantity * uses
            n_chemicals[input_chemical] = new_quantity

def get_fuel_unit(reactions, refined):
    refined_chemicals, refined_reactions = refined

    outputs = dict()
    for output_quantity, output_chemical in reactions.keys():
        outputs[output_chemical] = output_quantity

    fuel_recipe = reactions.get((1, "FUEL"))
    if fuel_recipe is None:
        return -1

    needed_chemicals = defaultdict(lambda: 0)
    for input_quantity, input_chemical in fuel_recipe:
        current_quantity = needed_chemicals[input_chemical]
        needed_chemicals[input_chemical] = current_quantity + input_quantity

    #print(dict(needed_chemicals))
    eec_args = needed_chemicals, refined_chemicals, outputs, reactions
    expand_expansion_chemicals(*eec_args)
    #print(dict(needed_chemicals))
    ores = 0
    expansion = defaultdict(lambda: 0)
    for needed_chemical, needed_quantity in needed_chemicals.items():
        if needed_chemical == "ORE":
            ores = ores + needed_quantity
            continue

        available_quantity = outputs.get(needed_chemical)
        if available_quantity is None:
            continue

        if needed_quantity >= available_quantity:
            uses = ceil(needed_quantity / available_quantity)

        else:
            uses = ceil(available_quantity / needed_quantity)

        reaction_key = available_quantity, needed_chemical
        expanded_reaction = reactions.get(reaction_key)
        if expanded_reaction:
            for expanded_quantity, expanded_chemical in expanded_reaction:
                used_quantity = expanded_quantity * uses
                if expanded_chemical == "ORE":
                    ores = ores + used_quantity
                    continue

                current_quantity = expansion[expanded_chemical]
                new_quantity = current_quantity + used_quantity
                expansion[expanded_chemical] = new_quantity

        else:
            current_quantity = expansion[needed_chemical]
            new_quantity = current_quantity + needed_quantity
            expansion[expanded_chemical] = new_quantity

    expansion = dict(expansion)
    refined_units = {rc: rq for rq, rc in refined_reactions.keys()}
    for chemical, quantity in expansion.items():
        if chemical == "ORE":
            ores = ores + quantity
            continue

        refined_unit = refined_units.get(chemical)
        refined_needed = ceil(quantity / refined_unit)
        refined_key = refined_unit, chemical
        refined_ore = refined_reactions.get(refined_key)
        ore_count = refined_ore * refined_needed
        ores = ores + ore_count

    return ores

if __name__ == "__main__":
    #reactions = parse_reactions("\n".join([
    #    "10 ORE => 10 A",
    #    "1 ORE => 1 B",
    #    "7 A, 1 B => 1 C",
    #    "7 A, 1 C => 1 D",
    #    "7 A, 1 D => 1 E",
    #    "7 A, 1 E => 1 FUEL"
    #]))
    #reactions = parse_reactions("\n".join([
    #    "9 ORE => 2 A",
    #    "8 ORE => 3 B",
    #    "7 ORE => 5 C",
    #    "3 A, 4 B => 1 AB",
    #    "5 B, 7 C => 1 BC",
    #    "4 C, 1 A => 1 CA",
    #    "2 AB, 3 BC, 4 CA => 1 FUEL"
    #]))
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
    reactions = parse_reactions("\n".join([
        "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
        "17 NVRVD, 3 JNWZP => 8 VPVL",
        "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
        "22 VJHF, 37 MNCFX => 5 FWMGM","139 ORE => 4 NVRVD",
        "144 ORE => 7 JNWZP",
        "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
        "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
        "145 ORE => 6 MNCFX",
        "1 NVRVD => 8 CXFTF",
        "1 VJHF, 6 MNCFX => 4 RFSQX",
        "176 ORE => 6 VJHF"
    ]))
    #reactions = parse_reactions(Path("aoc14.txt").read_text())
    #pprint(reactions)
    #print("----")
    refined = get_refined_chemicals(reactions)
    #print(refined)
    reactions = expand_reactions(reactions, refined)
    #pprint(reactions)
    #print("----")
    ores = get_fuel_unit(reactions, refined)
    #print("----")
    print(ores)
