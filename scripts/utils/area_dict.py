from .read_i2 import read_i2
from .read_gde import read_gde

def area_dict():
    descs = read_i2()
    data = read_gde()
    areas = {}
    remove_list = ['',"winterfair2022_shack","winterfair2022_icerink","winterfair2022_sledding","winterfair2022_ferriswheel","winterfair2022_train"]
    for line in data:
        if data[line].get("1081") == "Quest":
            area_key = data[line].get("20", "").lower()
            if area_key and area_key not in areas and area_key not in remove_list:
                area_desc_key = f"namekey_{area_key}" if f"namekey_{area_key}" in descs else f"questtitle_{area_key}"
                area_desc = descs.get(area_desc_key, "").lower()
                areas[area_key] = area_desc
    return areas