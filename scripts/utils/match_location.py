from .area_dict import area_dict

import difflib
import sys

def match_location(location):
    valid_areas = area_dict()
    if location.lower() in valid_areas.keys() or location.lower() in valid_areas.values():
        location = location.lower() if location.lower() in valid_areas.keys() else list(valid_areas.keys())[list(valid_areas.values()).index(location.lower())]
        return location
    else:    
        close_matches = difflib.get_close_matches(location, list(valid_areas.keys())+list(valid_areas.values()))
        if close_matches:
            choice = input(f"Did you mean '{close_matches[0]}'? (y/n)")
            if choice.lower() == "y":
                location = close_matches[0] if close_matches[0] in valid_areas.keys() else list(valid_areas.keys())[list(valid_areas.values()).index(close_matches[0])]
                return location
            else:
                print("Invalid area name.")
                sys.exit(1)
        else:
            print("Invalid area name.")
            sys.exit(1)