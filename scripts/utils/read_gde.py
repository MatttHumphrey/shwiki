import json
import os.path as path

GDE_DATA = path.join(path.dirname(path.dirname(path.dirname(__file__))),"data","gde_data.json")

def read_gde():
    with open(GDE_DATA, "r", encoding="utf8") as file:
        data = json.load(file)
    return data