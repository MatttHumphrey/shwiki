from .string_hash import string_hash
from .read_gde import read_gde

def area_tasks_dict():
    dic = {}
    data = read_gde()
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash[0]) == "Quest":
            area = data[line].get(stringhash[1]).lower()
            tasks = data[line].get(stringhash[2])
            if dic.get(area) == None:
                dic[area] = []
            dic[area].append(tasks)              
    return dic