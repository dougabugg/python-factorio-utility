import factorio
config_file = open("factorio_vanilla.config.json", "r", encoding="utf-8")
config = factorio.import_game_config(config_file)

def compute_unit_quantities(target_item, speed, raw_inputs):
    totals = config.compute_inputs(target_item, speed, raw_inputs)
    results = [(target_item, speed, config.compute_unit_quantity(target_item, speed, "ideal assembly"))]
    for item_name, count in totals.items():
        item = config.get_item(item_name)
        if len(item.producers) > 0:
            unit_name = None
            process_type = item.producers[0].process_type.name
            if process_type == "assembly":
                unit_name = "ideal assembly"
            elif process_type == "smelt":
                unit_name = "steel furnace"
            elif process_type == "chemical":
                unit_name = "chemical plant"
            elif process_type == "miner":
                unit_name = "electric mining drill"
            else:
                raise Exception(process_type)
            results.append((item_name, count, config.compute_unit_quantity(item_name, count, unit_name)))
        else:
            results.append((item_name, count, None))
    for i in results:
        print(i)
    return results

# print(compute_unit_quantities("green science", 2, ["iron", "copper"]))


(compute_unit_quantities("grey science", 2, ["iron", "copper", "steel"]))
print("\n")
(compute_unit_quantities("blue science", 2, ["iron", "copper", "steel"]))
print("\n")
(compute_unit_quantities("purple science", 2, ["iron", "copper", "steel", "stone", "brick"]))
print("\n")
(compute_unit_quantities("yellow science", 2, ["iron", "copper", "steel"]))
