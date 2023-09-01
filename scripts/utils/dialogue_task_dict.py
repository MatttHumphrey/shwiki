from .string_hash import string_hash
from .read_gde import read_gde

def dialogue_task_dict():
    task_dict = {}
    data = read_gde()
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"], "")
            if area not in task_dict:
                task_dict[area] = []
            dialogue_ids = [data[line].get(stringhash["CompleteDialogue"]), data[line].get(stringhash["OpenDialogue"])]
            task_dict[area].extend(task_id for task_id in dialogue_ids if task_id) 
    return task_dict