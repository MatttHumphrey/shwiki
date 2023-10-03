from .string_hash import string_hash
from .read_gde import read_gde

def area_tasks_dict():
    '''Returns a dictionary containing the names of every area and a list of all the tasks completed throughout that area.'''
    data = read_gde()
    stringhash = string_hash()
    task_dict = {}
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"]).lower()
            tasks = data[line].get(stringhash["Id"])
            if task_dict.get(area) == None:
                task_dict[area] = []
            task_dict[area].append(tasks)              
    return task_dict