items_by_category = {
    "logistics": {
        "storage": ["wooden-chest", "iron-chest", "steel-chest", "storage-tank"],
        "belt-transport": ["transport-belt", "fast-transport-belt", "express-transport-belt",
            "underground-belt", "fast-underground-belt", "express-underground-belt", "splitter",
            "fast-splitter", "express-splitter"],
        "inserters": ["burner-inserter", "inserter", "long-handed-inserter", "fast-inserter",
            "filter-inserter", "stack-inserter", "stack-filter-inserter"],
        "energy-and-pipe-distribution": ["small-electric-pole", "medium-electric-pole",
            "big-electric-pole", "substation", "pipe", "pipe-to-ground", "pump"],
        "railway": ["rail", "train-stop", "rail-signal", "rail-chain-signal", "locomotive",
            "cargo-wagon", "artillery-wagon"],
        "transport": ["car", "tank", "spidertron", "spidertron-remote"],
        "logistic-network": ["logistic-robot", "construction-robot", "active-provider-chest",
            "passive-provider-chest", "storage-chest", "buffer-chest", "requester-chest",
            "roboport"],
        "circuit-network": ["lamp", "red-wire", "green-wire", "arithmetic-combinator",
            "decider-combinator", "constant-combinator", "power-switch", "programmable-speaker"],
        "terrain": ["stone-brick", "concrete", "hazard-concrete", "refined-concrete",
            "refined-hazard-concrete", "landfill", "cliff-explosive"]
    },
    "production-items": {
        "tools": ["repair-pack"],
        "electricity": ["boiler", "steam-engine", "solar-panel", "accumulator", "nuclear-reactor",
            "heat-pipe", "heat-exchanger", "steam-turbine"],
        "resource-extraction": ["burner-mining-drill", "electric-mining-drill", "offshore-pump",
            "pumpjack"],
        "furnaces": ["stone-furnace", "steel-furnace", "electric-furnace"],
        "production": ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3",
            "oil-refinery", "chemical-plant", "centrifuge", "lab"],
        "modules": ["beacon", "speed-module", "speed-module-2", "speed-module-3",
            "efficiency-module", "efficiency-module-2", "efficiency-module-3",
            "productivity-module", "productivity-module-2", "productivity-module-3"],
        "space": ["rocket-silo", "satellite"]
    },
    "intermediate-products": {
        "fluids": ["crude-oil", "heavy-oil", "light-oil", "lubricant", "petroleum-gas",
            "sulfuric-acid", "water", "steam"],
        "resources": ["wood", "coal", "stone", "iron-ore", "copper-ore", "uranium-ore",
            "raw-fish"],
        "materials": ["iron-plate", "copper-plate", "solid-fuel", "steel-plate", "plastic-bar",
            "sulfur", "battery", "explosives"],
        "crafting-components": ["copper-cable", "iron-stick", "iron-gear-wheel",
            "electronic-circuit", "advanced-circuit", "processing-unit", "engine-unit",
            "electric-engine-unit", "flying-robot-frame", "rocket-part", "rocket-control-unit",
            "low-density-structure", "rocket-fuel", "nuclear-fuel", "uranium-235", "uranium-238",
            "uranium-fuel-cell", "used-up-uranium-fuel-cell"],
        "science-packs": ["automation-science-pack", "logistic-science-pack",
            "military-science-pack", "chemical-science-pack", "production-science-pack",
            "utility-science-pack", "space-science-pack"]
    },
    "combat-items": {
        "weapons": ["pistol", "submachine-gun", "shotgun", "combat-shotgun", "rocket-launcher",
            "flamethrower", "land-mine"],
        "ammo": ["firearm-magazine", "piercing-rounds-magazine", "uranium-rounds-magazine",
            "shotgun-shells", "piercing-shotgun-shells", "cannon-shell", "explosive-cannon-shell",
            "uranium-cannon-shell", "explosive-uranium-cannon-shell", "artillery-shell", "rocket",
            "explosive-rocket", "atomic-bomb", "flamethrower-ammo"],
        "capsules": ["grenade", "cluster-grenade", "poison-capsule", "slowdown-capsule",
            "defender-capsule", "distractor-capsule", "destroyer-capsule"],
        "armor": ["light-armor", "heavy-armor", "modular-armor",
            "power-armor", "power-armor-mk2"],
        "equipment-modules": ["portable-solar-panel", "portable-fusion-reactor",
            "personal-battery", "personal-battery-mk2", "belt-immunity-equipment", "exoskeleton",
            "personal-roboport", "personal-roboport-mk2", "nightvision"],
        "combat-equipment": ["energy-shield", "energy-shield-mk2", "personal-laser-defense",
            "discharge-defense", "discharge-defense-remote"],
        "defense": ["wall", "gate", "gun-turret", "laser-turret", "flamethrower-turret",
            "artillery-turret", "artillery-targeting-remote", "radar"]
    }
}

items = []
for category in items_by_category.values():
    for subcategory in category.values():
        items.extend(subcategory)

recipes = []
