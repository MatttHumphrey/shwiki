from .string_hash import string_hash
from .read_gde import read_gde
from .read_i2 import read_i2

def plant_dict():
    descs = read_i2()
    data = read_gde()
    stringhash = string_hash()
    plants = {}
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "PeriodicalEvent" and data[line].get(stringhash["ItemCategory"]).split("_")[0] == "Plant":
            plant_name = data[line].get(stringhash["ItemCategory"]).split("_")[1].lower()
            if plant_name and plant_name not in plants:
                plant_desc_key = f"categoryname_plant_{plant_name}"
                plant_desc = descs.get(plant_desc_key, "").lower()
                plants[plant_name] = plant_desc
    return plants