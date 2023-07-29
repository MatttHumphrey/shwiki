from read_gde import read_gde

def task_numbers(loc, id):
    data = read_gde()
    id_dict = {}
    n = 1
    for line in data:
        if data[line].get("1071") == "Quest" and data[line].get("18").lower() == loc:
            id_dict[data[line].get("2")] = f"{id}-{n}"
            n += 1
    return id_dict