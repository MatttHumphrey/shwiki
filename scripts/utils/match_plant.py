import difflib
import sys

from .read_data import read_gde, read_i2
from .string_hash import string_hash

def plant_dict():
    '''Generates a dictionary with all the endangered plants in the game files and their corresponding in game name.'''
    gde_data = read_gde()
    i2_data = read_i2()
    plants = {}
    stringhash = string_hash(gde_data)
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "PeriodicalEvent" and gde_data[line].get(stringhash["ItemCategory"]).split("_")[0] == "Plant":
            plant_name = gde_data[line].get(stringhash["ItemCategory"]).split("_")[1].lower()
            if plant_name and plant_name not in plants:
                plant_desc_key = f"categoryname_plant_{plant_name}"
                plant_desc = i2_data.get(plant_desc_key, "").lower()
                plants[plant_name] = plant_desc
    return plants

def match_plant(plant):
    '''
    Returns a correct in file endangered plant name from itself or its in game name.
    If neither are found, uses difflib to suggest possible corrections.

    Keyword Arguments:
    plant               - A string containing a possible plant name to be checked

    Return Value:
    String listing the plant's in file name.
    '''
    valid_plants = plant_dict()
    if plant.lower() in valid_plants:
        plant = plant.lower() if plant.lower() in valid_plants.keys() else list(valid_plants.keys())[list(valid_plants.values()).index(plant.lower())]
        return plant
    close_matches = difflib.get_close_matches(plant, list(valid_plants.keys())+list(valid_plants.values()))
    if close_matches:
        choice = input(f"Did you mean '{close_matches[0]}'? (y/n) ")
        if choice.lower() == "y":
            plant = close_matches[0] if close_matches[0] in valid_plants.keys() else list(valid_plants.keys())[list(valid_plants.values()).index(close_matches[0])]
            return plant
        print("Invalid plant name.")
        sys.exit(1)
    else:
        print("Invalid plant name.")
        sys.exit(1)
