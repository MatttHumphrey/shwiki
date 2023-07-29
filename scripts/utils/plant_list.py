from scripts.utils.read_i2 import read_i2
from scripts.utils.read_gde import read_gde

def plant_list():
    descs = read_i2()
    data = read_gde()
    plants = {}
    for line in data:
        if data[line].get("1071") == "PeriodicalEvent" and data[line].get("663").split("_")[0] == "Plant":
            plant_name = data[line].get("663").split("_")[1].lower()
            if plant_name and plant_name not in plants:
                plant_desc_key = f"categoryname_plant_{plant_name}"
                plant_desc = descs.get(plant_desc_key, "").lower()
                plants[plant_name] = plant_desc
    return plants