from .read_gde import read_gde
from .string_hash import string_hash

def task_numbers(loc, id, ):
    data = read_gde()
    stringhash = string_hash()
    id_dict = {}
    n = 1
    for line in data:
        if data[line].get(stringhash[0]) == "Quest" and data[line].get(stringhash[7]).lower() == loc:
            id_dict[data[line].get(stringhash[2])] = f"{id}-{n}"
            n += 1
    return id_dict