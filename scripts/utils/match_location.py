import difflib
import sys

from .read_data import read_gde, read_i2
from .string_hash import string_hash

REMOVE_LIST = set(['', "winterfair2022_shack", "winterfair2022_icerink", "winterfair2022_sledding",
                   "winterfair2022_ferriswheel", "winterfair2022_train"])

def area_dict(gde_data, i2_data):
    '''Generates a dictionary with all the areas in the game files and their in game names.
    
    Keyword Arguments:
    gde_data            - The gde_data dictionary
    i2_data             - The i2_data dictionary
    
    Return Value:
    A dictionary containing all the areas in the game files and their in game names.
    '''
    areas = {}
    stringhash = string_hash(gde_data)
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area_key = gde_data[line].get(stringhash["AreaGroupKey"], "").lower()
            if area_key and area_key not in areas and area_key not in REMOVE_LIST:
                area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in i2_data else f"questtitle_{area_key}"
                area_desc = i2_data.get(area_desc_key, "").lower()
                areas[area_key] = area_desc
    return areas

def match_location(location):
    '''
    Returns a correct in file area name from itself or its in game name.
    If neither are found, uses difflib to suggest possible corrections.

    Keyword Arguments:
    location            - A string containing a possible area name to be checked

    Return Value:
    String listing the area's in file name.
    '''
    gde_data = read_gde()
    i2_data = read_i2()
    valid_areas = area_dict(gde_data, i2_data)
    if location.lower() in valid_areas:
        location = location.lower() if location.lower() in valid_areas.keys() else list(valid_areas.keys())[list(valid_areas.values()).index(location.lower())]
        return location
    close_matches = difflib.get_close_matches(location, list(valid_areas.keys())+list(valid_areas.values()))
    if close_matches:
        choice = input(f"Did you mean '{close_matches[0]}'? (y/n)")
        if choice.lower() == "y":
            location = close_matches[0] if close_matches[0] in valid_areas.keys() else list(valid_areas.keys())[list(valid_areas.values()).index(close_matches[0])]
            return location
        print("Invalid area name.")
        sys.exit(1)
    else:
        print("Invalid area name.")
        sys.exit(1)
