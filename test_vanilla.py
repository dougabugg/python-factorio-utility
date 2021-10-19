import factorio
config_file = open("factorio_vanilla.config.json", "r", encoding="utf-8")
config = factorio.import_game_config(config_file)

def assert_raw_inputs(item, speed, raw_inputs):
    totals = config.compute_inputs(item, speed, raw_inputs.keys())
    for raw_item, expected_total in raw_inputs.items():
        assert totals[raw_item] == expected_total

assert_raw_inputs("red science", 1, {"iron": 2, "copper": 1})
assert_raw_inputs("green science", 1, {"iron": 5.5, "copper": 1.5})
assert_raw_inputs("grey science", 2, {"iron": 9, "copper": 5, "steel": 1, "coal": 10, "brick": 10})
assert_raw_inputs("blue science", 2, {"iron": 6, "copper": 15, "engine": 2, "plastic": 6, "sulfur": 1})

print("done. finished without errors")
