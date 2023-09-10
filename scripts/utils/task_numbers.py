from .string_hash import string_hash
from .read_gde import read_gde

def task_numbers(loc, id):
    data = read_gde()
    stringhash = string_hash()
    id_dict = {}
    n = 1
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest" and data[line].get(stringhash["CompleteAreaKey"]).lower() == loc:
            id_dict[data[line].get(stringhash["Id"])] = f"{id}-{n}"
            n += 1
    return id_dict