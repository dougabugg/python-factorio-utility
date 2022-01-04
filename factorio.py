class ProcessType:
    def __init__(self, name):
        self.name = name
        self.units = []
        self.recipes = []
    
    def __repr__(self):
        return self.name

class ProcessUnit:
    def __init__(self, name, process_type, speed):
        self.name = name
        self.process_type = process_type
        self.speed = speed
    
    def __repr__(self):
        return "name: {}, process type: {}, speed: {};".format(
            self.name, self.process_type, self.speed)

class Item:
    def __init__(self, name):
        self.name = name
        self.producers = []
        self.consumers = []
    
    def get_default_producer(self):
        r = None
        for recipe in self.producers:
            if r is None or recipe.priority > r.priority:
                r = recipe
        return r

    def __repr__(self):
        return self.name

class Recipe:
    def __init__(self, inputs, outputs, craft_time, priority, process_type):
        self.inputs = inputs
        self.outputs = outputs
        self.craft_time = craft_time
        self.priority = priority
        self.process_type = process_type
    
    def get_input_count(self, item_name):
        count = None
        for c, item in self.inputs:
            if item.name == item_name:
                count = c
        if count is None:
            raise KeyError(item_name)
        else:
            return count
    
    def get_output_count(self, item_name):
        count = None
        for c, item in self.outputs:
            if item.name == item_name:
                count = c
        if count is None:
            raise KeyError(item_name)
        else:
            return count

    def __repr__(self):
        return "outputs: {}, inputs: {}, craft time: {}, priority: {}, process type: {};".format(
            self.outputs, self.inputs, self.craft_time, self.priority, self.process_type)

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
    
    def get_item(self, name):
        try:
            return self.named_items[name]
        except KeyError as e:
            raise GameConfigError('no item with name "{}" exists'.format(name)) from e
    
    def get_process_type(self, name):
        try:
            return self.named_process_types[name]
        except KeyError as e:
            raise GameConfigError('no process type with name "{}" exists'.format(name)) from e
    
    def get_process_unit(self, name):
        try:
            return self.named_process_units[name]
        except KeyError as e:
            raise GameConfigError('no process unit with name "{}" exists'.format(name)) from e

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
        norm_process_type = self.get_process_type(process_type)
        unit = ProcessUnit(name, norm_process_type, speed)
        norm_process_type.units.append(unit)
        self.process_units.append(unit)
        self.named_process_units[name] = unit

    def add_recipe(self, inputs, outputs, craft_time, priority, process_type):
        norm_inputs = []
        for count, item_name in inputs:
            norm_inputs.append((count, self.get_item(item_name)))
        norm_outputs = []
        for count, item_name in outputs:
            norm_outputs.append((count, self.get_item(item_name)))
        norm_process_type = self.get_process_type(process_type)
        recipe = Recipe(norm_inputs, norm_outputs, craft_time, priority, norm_process_type)
        norm_process_type.recipes.append(recipe)
        for count, item in norm_inputs:
            item.consumers.append(recipe)
        for count, item in norm_outputs:
            item.producers.append(recipe)
    
    def compute_inputs(self, target_item_name, target_speed, raw_item_names=None):
        raw_items = None
        if not raw_item_names is None:
            raw_items = set((self.get_item(name) for name in raw_item_names))
        return compute_inputs(self.get_item(target_item_name), target_speed, raw_items)
    
    def compute_unit_quantity(self, target_item_name, target_speed, target_unit_name):
        unit = self.get_process_unit(target_unit_name)
        item = self.get_item(target_item_name)
        recipe = item.producers[0]
        assert recipe.process_type == unit.process_type
        return (recipe.craft_time / recipe.get_output_count(item.name) * target_speed) / unit.speed

def import_game_config(fp):
    import json
    raw_config = json.load(fp)
    config = GameConfig()
    for name in raw_config["items"]:
        config.add_item(name)
    for name in raw_config["process_types"]:
        config.add_process_type(name)
    for raw_unit in raw_config["process_units"]:
        config.add_process_unit(raw_unit["name"], raw_unit["process_type"], raw_unit["speed"])
    for recipe in raw_config["recipes"]:
        config.add_recipe(recipe["inputs"], recipe["outputs"], recipe["craft_time"], recipe["priority"], recipe["process_type"])
    return config

def compute_inputs(target_item, target_speed, raw_items=None):
    recipe = None
    # use recipe with highest priority
    for r in target_item.producers:
        if recipe is None or recipe.priority < r.priority:
            recipe = r
    if recipe is None:
        return {}
    output_count = recipe.get_output_count(target_item.name)
    totals = {}
    for count, item in recipe.inputs:
        speed = count / output_count * target_speed
        totals[item.name] = totals.get(item.name, 0) + speed
        if raw_items is None or not item in raw_items:
            sub_totals = compute_inputs(item, speed, raw_items)
            # print("for {}".format(item.name), sub_totals)
            for item_name, total in sub_totals.items():
                totals[item_name] = totals.get(item_name, 0) + total
    return totals

class BaseMachine:
    """A base, abstract machine"""
    def compute_inputs(self):
        raise NotImplemented
    
    def compute_outputs(self):
        raise NotImplemented

class Machine(BaseMachine):
    """A collection of one or more identical machines, configured for the same recipe"""
    def __init__(self, process_unit, recipe, count=1):
        assert process_unit.process_type == recipe.process_type
        self.process_unit = process_unit
        self.recipe = recipe
        self.count = count
    
    def compute_inputs(self):
        r = dict()
        for c, input in self.recipe.inputs:
            r[input.name] = c * self.process_unit.speed * self.count
        return r
    
    def compute_outputs(self):
        r = dict()
        for c, output in self.recipe.outputs:
            r[output.name] = c * self.process_unit.speed * self.count
        return r

class Factory(BaseMachine):
    """A logical group of zero or more different machines"""
    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def compute_inputs(self):
        r = dict()
        for machine in self.machines:
            for item, count in machine.compute_inputs().items():
                r[item] = r.get(item, 0) + count
        return r

    def compute_outputs(self):
        r = dict()
        for machine in self.machines:
            for item, count in machine.compute_outputs().items():
                r[item] = r.get(item, 0) + count
        return r
