from .string_hash import string_hash
from .read_gde import read_gde
from .read_i2 import read_i2

def area_dict():
    descs = read_i2()
    data = read_gde()
    stringhash = string_hash()
    areas = {}
    remove_list = ['',"winterfair2022_shack","winterfair2022_icerink","winterfair2022_sledding","winterfair2022_ferriswheel","winterfair2022_train"]
    for line in data:
        if data[line].get(stringhash[0]) == "Quest":
            area_key = data[line].get(stringhash[1], "").lower()
            if area_key and area_key not in areas and area_key not in remove_list:
                area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in descs else f"questtitle_{area_key}"
                area_desc = descs.get(area_desc_key, "").lower()
                areas[area_key] = area_desc
    return areas