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

def get_dependencies(reactions):
    outputs = dict()
    for output_quantity, output_chemical in reactions.keys():
        outputs[output_chemical] = output_quantity

    top_down = dict()
    bottom_up = defaultdict(list)
    refined_ore = list()
    for chemical, quantity in outputs.items():
        available_quantity = outputs.get(chemical)
        reaction = reactions.get((available_quantity, chemical))
        #print(quantity, chemical, reaction)
        dependencies = [chem for quan, chem in reaction]
        if len(dependencies) == 1 and dependencies[0] == "ORE":
            refined_ore.append(chemical)

        for dep in dependencies:
            bottom_up[dep].append(chemical)

        top_down[chemical] = dependencies
            
    deps = dict()
    deps["td"] = top_down
    deps["bu"] = bottom_up
    deps["ro"] = refined_ore
    deps["os"] = outputs
    return deps

def apply_substitions(reactions, dependencies):
    outputs = dependencies.get("os")
    sub_reactions = deepcopy(reactions)
    changed = True
    while changed:
        changed = False
        for reaction_output, reaction_inputs in sub_reactions.items():
            output_quantity, output_chemical = reaction_output
            substitutions = list()
            for reaction_input in reaction_inputs:
                input_quantity, input_chemical = reaction_input
                if input_chemical == "ORE":
                    substitutions.append(reaction_input)
                    continue

                reaction_match = reactions.get(reaction_input)
                if not reaction_match:
                    available_quantity = outputs.get(input_chemical)
                    used = input_quantity // available_quantity
                    if used == 0 or input_quantity % available_quantity != 0: 
                        substitutions.append(reaction_input)
                        continue

                    match_key = available_quantity, input_chemical
                    reaction_match = deepcopy(reactions.get(match_key))
                    for rm, r_match in enumerate(reaction_match):
                        r_quantity, r_chemical = r_match
                        reaction_match[rm] = r_quantity * used, r_chemical

                changed = True
                substitutions.extend(reaction_match)

            condensed = defaultdict(lambda: 0)
            for substitution in substitutions:
                sub_quantity, sub_chemical = substitution
                current_quantity = condensed[sub_chemical]
                condensed[sub_chemical] = current_quantity + sub_quantity

            substituted = [(q, c) for c, q in condensed.items()]
            sub_reactions[reaction_output] = substituted

    processed = set(outputs.keys())
    for sub_inputs in sub_reactions.values():
        for sub_quantity, sub_chemical in sub_inputs:
            if sub_chemical in processed:
                processed.remove(sub_chemical)

    dependencies["pc"] = processed
    return sub_reactions

def expand_reactions(reactions, dependencies):
    top_down = dependencies.get("td")
    bottom_up = dependencies.get("bu")
    refined_ore = dependencies.get("ro")
    outputs = dependencies.get("os")
    processed = dependencies.get("pc")

    fuel_key = 1, "FUEL"
    expanded_reactions = deepcopy(reactions)
    changed = True
    while changed:
        changed = False
        expansions = list()
        for reaction_input in expanded_reactions.get(fuel_key):
            input_quantity, input_chemical = reaction_input
            if input_chemical == "ORE":
                expansions.append(reaction_input)
                continue

            deps = top_down.get(input_chemical)
            needed = bottom_up.get(input_chemical)
            skip = False
            for need in needed:
                if need not in processed:
                    skip = True
                    break

            if skip:
                expansions.append(reaction_input)
                continue

            available_quantity = outputs.get(input_chemical)
            used = ceil(input_quantity / available_quantity)

            match_key = available_quantity, input_chemical
            reaction_match = deepcopy(reactions.get(match_key))
            for rm, r_match in enumerate(reaction_match):
                r_quantity, r_chemical = r_match
                reaction_match[rm] = r_quantity * used, r_chemical

            changed = True
            expansions.extend(reaction_match)

        condensed = defaultdict(lambda: 0)
        for expansion in expansions:
            exp_quantity, exp_chemical = expansion
            current_quantity = condensed[exp_chemical]
            condensed[exp_chemical] = current_quantity + exp_quantity

        expanded = [(q, c) for c, q in condensed.items()]
        expanded_reactions[fuel_key] = expanded
        processed.add(input_chemical)

    return expanded_reactions

def get_fuel_unit(reactions, dependencies):
    outputs = dependencies.get("os")

    fuel_key = 1, "FUEL"
    ores = 0
    for reaction_input in reactions.get(fuel_key):
        input_quantity, input_chemical = reaction_input
        if input_chemical == "ORE":
            ores = ores + input_quantity
            continue

        available_quantity = outputs.get(input_chemical)
        if input_quantity >= available_quantity:
            used = ceil(input_quantity / available_quantity)

        else:
            used = available_quantity

        match_key = available_quantity, input_chemical
        reaction_match = deepcopy(reactions.get(match_key))
        for rm, r_match in enumerate(reaction_match):
            r_quantity, r_chemical = r_match
            ores = ores + r_quantity * used

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
    deps = get_dependencies(reactions)
    pprint(reactions)
    print("----")
    reactions = apply_substitions(reactions, deps)
    pprint(reactions)
    print("----")
    reactions = expand_reactions(reactions, deps)
    pprint(reactions)
    print("----")
    ores = get_fuel_unit(reactions, deps)
    print(ores)
