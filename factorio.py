class ProcessType:
    def __init__(self, name):
        self.name = name
        self.units = []
        self.recipes = []

class ProcessUnit:
    def __init__(self, name, process_type, speed):
        self.name = name
        self.process_type = process_type
        self.speed = speed

class Item:
    def __init__(self, name):
        self.name = name
        self.producers = []
        self.consumers = []

class Recipe:
    def __init__(self, inputs, outputs, craft_time, priority, process_type):
        self.inputs = inputs
        self.outputs = outputs
        self.craft_time = craft_time
        self.priority = priority
        self.process_type = process_type

class GameConfigError(Exception):
    pass

class GameConfig:
    def __init__(self):
        self.items = []
        self.named_items = {}
        self.recipes = []
        self.process_types = []
        self.named_process_types = {}
        self.process_units = []
        self.named_process_units = {}
    
    def add_item(self, name):
        item = Item(name)
        if name in self.named_items:
            raise GameConfigError('item with name "{}" already exists'.format(name))
        self.items.append(item)
        self.named_items[name] = item
    
    def add_process_type(self, name):
        process_type = ProcessType(name)
        if name in self.named_process_types:
            raise GameConfigError('process type with name "{}" already exists'.format(name))
        self.process_types.append(process_type)
        self.named_process_types[name] = process_type
    
    def add_process_unit(self, name, process_type, speed):
        norm_process_type = self.named_process_types[process_type]
        unit = ProcessUnit(name, norm_process_type, speed)
        norm_process_type.units.append(unit)
        self.process_units.append(unit)
        self.named_process_units[name] = unit

    def add_recipe(self, inputs, outputs, craft_time, priority, process_type):
        norm_inputs = []
        for count, item_name in inputs:
            norm_inputs.append((count, self.named_items[item_name]))
        norm_outputs = []
        for count, item_name in outputs:
            norm_outputs.append((count, self.named_items[item_name]))
        norm_process_type = self.named_process_types[process_type]
        recipe = Recipe(norm_inputs, norm_outputs, craft_time, priority, norm_process_type)
        norm_process_type.recipes.append(recipe)
        for count, item in norm_inputs:
            item.producers.append(recipe)
        for count, item in norm_outputs:
            item.consumers.append(recipe)

def import_game_config(fp):
    import json
    raw_config = json.load(fp)
    config = GameConfig()
    for name in raw_config["items"]:
        config.add_item(name)
    for name in raw_config["process_type"]:
        config.add_process_type(name)
    for raw_unit in raw_config["process_units"]:
        config.add_process_unit(raw_unit["name"], raw_unit["process_type"], raw_unit["speed"])
    for recipe in raw_config["recipes"]:
        config.add_recipe(recipe["inputs"], recipe["outputs"], recipe["craft_time"], recipe["priority"], recipe["process_type"])
    return config
