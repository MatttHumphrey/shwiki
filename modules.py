import json
import os.path as path
from datetime import datetime

I2_FILE = path.join(path.dirname(__file__),"i2subset_english.json")
GDE_FILE = path.join(path.dirname(__file__),"gde_data.json")

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
                if area_key != "" and area_key not in valid_areas:
                    area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in descs else f"questtitle_{area_key}"
                    area_desc = descs.get(area_desc_key, "").lower()
                    if area_desc:
                        valid_areas[area_key] = area_desc
    return valid_areas

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