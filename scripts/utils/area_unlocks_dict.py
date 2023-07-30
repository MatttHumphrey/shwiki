from .read_gde import read_gde

def area_unlocks_dict():
    dic = {}
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            area = data[line].get("20").lower()
            unlocks = data[line].get("5")
            if dic.get(area) == None:
                dic[area] = []
            for item in unlocks:
                dic[area].append(item)              
    return dic