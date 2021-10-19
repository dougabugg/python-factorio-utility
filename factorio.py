class ProcessType:
    def __init__(self, name):
        self.name = name

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
    
    def add_recipe(self, inputs, outputs, craft_time, priority, process_type):
        norm_inputs = []
        for count, item_name in inputs:
            norm_inputs.append((count, self.named_items[item_name]))
        norm_outputs = []
        for count, item_name in outputs:
            norm_outputs.append((count, self.named_items[item_name]))
        recipe = Recipe(norm_inputs, norm_outputs, craft_time, priority, self.named_process_types[process_type])
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
    for recipe in raw_config["recipes"]:
        config.add_recipe(recipe["inputs"], recipe["outputs"], recipe["craft_time"], recipe["priority"], recipe["process_type"])
    return config


