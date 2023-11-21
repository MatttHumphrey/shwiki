import difflib
import sys

from .string_hash import string_hash
from .read_data import read_gde
from .read_data import read_i2

def area_dict():
    '''Generates a dictionary with all the areas in the game files and their in game names.'''
    areas = {}
    descriptions = read_i2()
    data = read_gde()
    stringhash = string_hash()
    remove_list = ['', "winterfair2022_shack", "winterfair2022_icerink", "winterfair2022_sledding",
                   "winterfair2022_ferriswheel", "winterfair2022_train"]
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area_key = data[line].get(stringhash["AreaGroupKey"], "").lower()
            if area_key and area_key not in areas and area_key not in remove_list:
                area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in descriptions else f"questtitle_{area_key}"
                area_desc = descriptions.get(area_desc_key, "").lower()
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
    valid_areas = area_dict()
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
