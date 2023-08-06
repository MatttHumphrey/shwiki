from .read_gde import read_gde
from .string_hash import string_hash

def dialogue_task_dict():
    task_dict = {}
    data = read_gde()
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash[0]) == "Quest":
            area = data[line].get(stringhash[1], "")
            if area not in task_dict:
                task_dict[area] = []
            dialogue_ids = [data[line].get(stringhash[4]), data[line].get(stringhash[5])]
            task_dict[area].extend(task_id for task_id in dialogue_ids if task_id) 
    return task_dict