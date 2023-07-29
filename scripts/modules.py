import json
import difflib
import sys
import os.path as path
from datetime import datetime

I2_FILE = path.join(path.join(path.dirname(path.dirname(__file__)),"data"),"i2subset_english.json")
GDE_FILE = path.join(path.join(path.dirname(path.dirname(__file__)),"data"),"gde_data.json")

def read_i2():
    descriptions = {}
    with open(I2_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            descriptions[line.get("Term").lower()] = line.get("Languages")[0].replace("\n", " ").replace("\"", '"')
    return descriptions

def tasknumbers(loc, id):
    id_dict = {}
    n = 1
    with open(GDE_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest" and data[line].get("18").lower() == loc:
                id_dict[data[line].get("2")] = f"{id}-{n}"
                n += 1
    return id_dict

def get_arealist():
    descs = read_i2()
    valid_areas = {}
    with open(GDE_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                area_key = data[line].get("20", "").lower()
                if area_key and area_key not in valid_areas:
                    area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in descs else f"questtitle_{area_key}"
                    area_desc = descs.get(area_desc_key, "").lower()
                    valid_areas[area_key] = area_desc
    return valid_areas

def get_plantlist():
    descs = read_i2()
    valid_plants = {}
    with open(GDE_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "PeriodicalEvent" and data[line].get("663").split("_")[0] == "Plant":
                plant_name = data[line].get("663").split("_")[1].lower()
                if plant_name and plant_name not in valid_plants:
                    plant_desc_key = f"categoryname_plant_{plant_name}"
                    valid_plants[plant_name] = plant_desc_key
    return valid_plants

def convert_date_format(input_date):
    date_object = datetime.strptime(input_date, '%Y%m%d')
    suffix = 'th' if 11 <= int(date_object.day) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(date_object.day % 10, 'th')
    return date_object.strftime('%B %d{}, %Y').format(suffix)

def task_dic():
    dic = {}
    with open(GDE_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                area = data[line].get("20", "")
                if area not in dic:
                    dic[area] = []
                task_ids = [data[line].get("36"), data[line].get("38")]
                dic[area].extend(task_id for task_id in task_ids if task_id) 
    return dic

def locate_task(key,dic):
    for area, task in dic.items():
        if key in task:
            return area
    return None

def match_location(location):
    valid_areas = get_arealist()
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

def match_plant(plant):
    valid_plants = get_plantlist()
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

def get_output_file(file):
    parent_dir = path.dirname(path.dirname(__file__))
    output_dir = path.join(path.join(parent_dir,"output"),file)
    return output_dir
