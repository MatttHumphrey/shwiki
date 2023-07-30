from scripts.utils.plant_dict import plant_dict
import difflib
import sys

def match_plant(plant):
    valid_plants = plant_dict()
    if plant.lower() in valid_plants.keys() or plant.lower() in valid_plants.values():
        plant = plant.lower() if plant.lower() in valid_plants.keys() else list(valid_plants.keys())[list(valid_plants.values()).index(plant.lower())]
        return plant
    else:    
        close_matches = difflib.get_close_matches(plant, list(valid_plants.keys())+list(valid_plants.values()))
        if close_matches:
            choice = input(f"Did you mean '{close_matches[0]}'? (y/n) ")
            if choice.lower() == "y":
                plant = close_matches[0] if close_matches[0] in valid_plants.keys() else list(valid_plants.keys())[list(valid_plants.values()).index(close_matches[0])]
                return plant
            else:
                print("Invalid plant name.")
                sys.exit(1)
        else:
            print("Invalid plant name.")
            sys.exit(1)