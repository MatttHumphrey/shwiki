from os import path
import json

GDE_DATA = path.join(path.dirname(path.dirname(path.dirname(__file__))),"data","gde_data.json")
I2_FILE = path.join(path.dirname(path.dirname(path.dirname(__file__))),"data","i2subset_english.json")

def read_gde():
    '''Reads data from gde_data.json into the script.'''
    with open(GDE_DATA, "r", encoding="utf8") as file:
        data = json.load(file)
    return data

def read_i2():
    '''Reads data from i2subset_english.json into the script.'''
    descriptions = {}
    with open(I2_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            descriptions[line.get("Term").lower()] = line.get("Languages")[0].replace("\n", " ").replace("\"", '"')
    return descriptions
