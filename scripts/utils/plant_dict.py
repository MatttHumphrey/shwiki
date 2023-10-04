from .string_hash import string_hash
from .read_gde import read_gde
from .read_i2 import read_i2

def plant_dict():
    '''Generates a dictionary with all the endangered plants in the game files and their corresponding in game name.'''
    data = read_gde()
    descriptions = read_i2()
    plants = {}
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "PeriodicalEvent" and data[line].get(stringhash["ItemCategory"]).split("_")[0] == "Plant":
            plant_name = data[line].get(stringhash["ItemCategory"]).split("_")[1].lower()
            if plant_name and plant_name not in plants:
                plant_desc_key = f"categoryname_plant_{plant_name}"
                plant_desc = descriptions.get(plant_desc_key, "").lower()
                plants[plant_name] = plant_desc
    return plants
