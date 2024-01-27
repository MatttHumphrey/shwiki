from .string_hash import string_hash
from .read_data import read_gde

def area_tasks_dict():
    '''Returns a dictionary containing the names of every area and a list of all the tasks completed throughout that area.'''
    data = read_gde()
    stringhash = string_hash()
    task_dict = {}
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"]).lower()
            tasks = data[line].get(stringhash["Id"])
            if task_dict.get(area) is None:
                task_dict[area] = []
            task_dict[area].append(tasks)
    return task_dict

def area_unlocks_dict():
    '''Returns a dictionary containing the names of every area and a list of all the tasks unlocked throughout that area.'''
    data = read_gde()
    stringhash = string_hash()
    unlocks_dict = {}
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"]).lower()
            unlocks = data[line].get(stringhash["CompleteOpenQuest"])
            if unlocks_dict.get(area) is None:
                unlocks_dict[area] = []
            for item in unlocks:
                unlocks_dict[area].append(item)
    return unlocks_dict

def dialogue_task_dict():
    '''Returns a dictionary containing the name of every area, and a list of their tasks that trigger dialogue.'''
    data = read_gde()
    stringhash = string_hash()
    task_dict = {}
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"], "")
            if area not in task_dict:
                task_dict[area] = []
            dialogue_ids = [data[line].get(stringhash["CompleteDialogue"]), data[line].get(stringhash["OpenDialogue"])]
            task_dict[area].extend(task_id for task_id in dialogue_ids if task_id)
    return task_dict

def locate_task(key, task_dict):
    '''
    Returns the area that a specified task is found in using a task_dict.
    
    Keyword Arguments:
    key                 - Id of task to locate
    task_dict           - Dictionary of tasks from dialogue_task_dict.py

    Return Value:
    Area returned as a string if found, or None value otherwise.
    '''
    for area, task in task_dict.items():
        if key in task:
            return area
    return None