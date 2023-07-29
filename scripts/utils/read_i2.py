import os.path as path
import json

I2_FILE = path.join(path.dirname(path.dirname(path.dirname(__file__))),"data","i2subset_english.json")

def read_i2():
    descriptions = {}
    with open(I2_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            descriptions[line.get("Term").lower()] = line.get("Languages")[0].replace("\n", " ").replace("\"", '"')
    return descriptions