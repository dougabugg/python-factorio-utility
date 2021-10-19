import factorio
config_file = open("factorio_vanilla.config.json", "r", encoding="utf-8")
config = factorio.import_game_config(config_file)
print("done. finished without errors")
