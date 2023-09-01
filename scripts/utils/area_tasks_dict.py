from .string_hash import string_hash
from .read_gde import read_gde

def area_tasks_dict():
    dic = {}
    data = read_gde()
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"]).lower()
            tasks = data[line].get(stringhash["Id"])
            if dic.get(area) == None:
                dic[area] = []
            dic[area].append(tasks)              
    return dic