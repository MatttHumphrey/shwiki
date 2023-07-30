from scripts.utils.read_i2 import read_i2
from scripts.utils.read_gde import read_gde

def area_dict():
    descs = read_i2()
    data = read_gde()
    areas = {}
    for line in data:
        if data[line].get("1071") == "Quest":
            area_key = data[line].get("20", "").lower()
            if area_key and area_key not in areas:
                area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in descs else f"questtitle_{area_key}"
                area_desc = descs.get(area_desc_key, "").lower()
                areas[area_key] = area_desc
    return areas