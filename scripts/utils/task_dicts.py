from .string_hash import string_hash

def area_tasks_dict(gde_data):
    '''Returns a dictionary containing the names of every area and a list of all the tasks completed throughout that area.'''
    stringhash = string_hash(gde_data)
    task_dict = {}
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = gde_data[line].get(stringhash["AreaGroupKey"]).lower()
            tasks = gde_data[line].get(stringhash["Id"])
            if task_dict.get(area) is None:
                task_dict[area] = []
            task_dict[area].append(tasks)
    return task_dict

def area_unlocks_dict(gde_data):
    '''Returns a dictionary containing the names of every area and a list of all the tasks unlocked throughout that area.'''
    stringhash = string_hash(gde_data)
    unlocks_dict = {}
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = gde_data[line].get(stringhash["AreaGroupKey"]).lower()
            unlocks = gde_data[line].get(stringhash["CompleteOpenQuest"])
            if unlocks_dict.get(area) is None:
                unlocks_dict[area] = []
            for item in unlocks:
                unlocks_dict[area].append(item)
    return unlocks_dict

def dialogue_task_dict(gde_data):
    '''Returns a dictionary containing the name of every area, and a list of their tasks that trigger dialogue.'''
    stringhash = string_hash(gde_data)
    task_dict = {}
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = gde_data[line].get(stringhash["AreaGroupKey"], "")
            if area not in task_dict:
                task_dict[area] = []
            dialogue_ids = [gde_data[line].get(stringhash["CompleteDialogue"]), gde_data[line].get(stringhash["OpenDialogue"])]
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
